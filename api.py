from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile
import json
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from resume_classifier import DocumentProcessor, ResumeClassifier

# Create FastAPI app
app = FastAPI(
    title="Resume Classifier API",
    description="API for classifying whether a document is a resume or not",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the classifier
processor = DocumentProcessor()
classifier = ResumeClassifier()

# Training data directory
TRAINING_DIR = "training_data"

# Response model
class ClassificationResponse(BaseModel):
    filename: str
    is_resume: bool
    confidence: float
    word_count: int
    keyword_density: float
    detected_keywords: list[str]
    timestamp: str

@app.on_event("startup")
async def startup_event():
    """Initialize the classifier with training data on startup."""
    # Check if training data exists
    if not os.path.exists(TRAINING_DIR):
        print("Generating training dataset...")
        from generate_training_data import create_training_dataset
        create_training_dataset(TRAINING_DIR, num_samples=50)
    
    # Load labels
    with open(os.path.join(TRAINING_DIR, 'labels.json'), 'r') as f:
        labels = json.load(f)
    
    # Load documents and prepare training data
    documents = []
    for filename, label in labels.items():
        file_path = os.path.join(TRAINING_DIR, filename)
        content = processor.read_file(file_path)
        if content:
            documents.append((content, label))
    
    print(f"Training classifier with {len(documents)} documents...")
    classifier.train(documents)
    print("Classifier training completed!")

@app.post("/classify/", response_model=ClassificationResponse)
async def classify_document(file: UploadFile = File(...)):
    """
    Upload a document and classify whether it's a resume or not.
    Accepts PDF, DOCX, and TXT files.
    """
    # Validate file extension
    allowed_extensions = {'.pdf', '.docx', '.txt'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format. Allowed formats: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Create a temporary file to store the upload
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            # Write uploaded file content to temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Process the document
            document_text = processor.read_file(temp_file.name)
            if not document_text:
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract text from the document"
                )
            
            # Make prediction
            prediction, confidence = classifier.predict(document_text)
            
            # Extract features
            processed_text = processor.preprocess_text(document_text)
            features = processor.extract_features(processed_text)
            
            # Get detected keywords
            resume_words = sorted(set(
                word for word in processed_text.split() 
                if word in processor.resume_keywords
            ))
            
            # Prepare response
            response = ClassificationResponse(
                filename=file.filename,
                is_resume=bool(prediction),
                confidence=float(confidence),
                word_count=features['word_count'],
                keyword_density=float(features['keyword_density']),
                detected_keywords=resume_words,
                timestamp=datetime.now().isoformat()
            )
            
            return response
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )
    
    finally:
        # Clean up the temporary file
        if 'temp_file' in locals():
            os.unlink(temp_file.name)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    # Run the FastAPI server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    )

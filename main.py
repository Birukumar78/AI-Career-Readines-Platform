from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from pypdf import PdfReader

from database import engine, Base, SessionLocal
from models.profile import Profile


app = FastAPI(
    title="AI Career Readines Platform",
    description="Backend API for AI-powered career readines and employability platform",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home API
@app.get("/")
def home():
    return {
        "message": "AI Career Readines API is running"
    }


# Database connection test
@app.get("/database-test")
def database_test():
    try:
        with engine.connect():
            return {
                "status": "success",
                "message": "PostgreSQL connected successfully"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# Create Profile API
@app.post("/profiles")
def create_profile(
    name: str,
    email: str,
    phone: str = None,
    education: str = None,
    college: str = None,
    degree: str = None,
    graduation_year: int = None,
    career_goal: str = None,
    db: Session = Depends(get_db)
):
    profile = Profile(
        name=name,
        email=email,
        phone=phone,
        education=education,
        college=college,
        degree=degree,
        graduation_year=graduation_year,
        career_goal=career_goal
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile

# Get All Profiles API
@app.get("/profiles")
def get_profiles(db: Session = Depends(get_db)):
    profiles = db.query(Profile).all()
    return profiles

# Get Single Profile API
@app.get("/profiles/{profile_id}")
def get_profile(profile_id: int, db: Session = Depends(get_db)):
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if profile is None:
         return {"message": "Profile not found"}
        return profile
    
    # Update Profile API
    # Update Profile API
@app.put("/profiles/{profile_id}")
def update_profile(
    profile_id: int,
    name: str,
    email: str,
    phone: str = None,
    education: str = None,
    college: str = None,
    degree: str = None,
    graduation_year: int = None,
    career_goal: str = None,
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if profile is None:
        return {"message": "Profile not found"}

    profile.name = name
    profile.email = email
    profile.phone = phone
    profile.education = education
    profile.college = college
    profile.degree = degree
    profile.graduation_year = graduation_year
    profile.career_goal = career_goal

    db.commit()
    db.refresh(profile)

    return profile

# Delete Profile API
@app.delete("/profiles/{profile_id}")
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if profile is None:
        return {"message": "Profile not found"}

    db.delete(profile)
    db.commit()

    return {"message": "Profile deleted successfully"}

# Resume Upload API
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "status": "success",
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "path": file_path
    }
    
    # Extract Resume Text API
# Extract Resume Text API
@app.post("/extract-resume-text")
async def extract_resume_text(
    profile_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    reader = PdfReader(file_path)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text + "\n"

    # Find profile
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if profile is None:
        return {
            "status": "error",
            "message": "Profile not found"
        }

    # Save resume text in database
    profile.resume_text = resume_text

    db.commit()
    db.refresh(profile)

    return {
        "status": "success",
        "message": "Resume text extracted and saved successfully",
        "profile_id": profile_id,
        "filename": file.filename,
        "resume_text": resume_text
    }
    
    # Resume Analysis API
@app.get("/analyze-resume/{profile_id}")
def analyze_resume(
    profile_id: int,
    db: Session = Depends(get_db)
):
    # Find profile
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if profile is None:
        return {
            "status": "error",
            "message": "Profile not found"
        }

    # Check resume text
    if not profile.resume_text:
        return {
            "status": "error",
            "message": "Resume text not found. Please upload and extract resume first."
        }

    resume_text = profile.resume_text.lower()

    # Skills to check
    skill_list = [
        "python",
        "c",
        "c++",
        "html",
        "css",
        "javascript",
        "java",
        "sql",
        "data analysis",
        "frontend development",
        "backend development",
        "machine learning",
        "fastapi",
        "django",
        "git"
    ]

    detected_skills = []

    for skill in skill_list:
        if skill in resume_text:
            detected_skills.append(skill)

    return {
        "status": "success",
        "profile_id": profile_id,
        "name": profile.name,
        "career_goal": profile.career_goal,
        "detected_skills": detected_skills,
        "total_skills": len(detected_skills)
    }
    
    # Skill Gap Analysis API
@app.get("/skill-gap/{profile_id}")
def skill_gap_analysis(
    profile_id: int,
    db: Session = Depends(get_db)
):
    # Find profile
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if profile is None:
        return {
            "status": "error",
            "message": "Profile not found"
        }

    # Check resume
    if not profile.resume_text:
        return {
            "status": "error",
            "message": "Resume text not found. Please upload and extract resume first."
        }

    resume_text = profile.resume_text.lower()

    # Detect current skills
    skill_list = [
        "python",
        "c",
        "c++",
        "html",
        "css",
        "javascript",
        "java",
        "data analysis",
        "frontend development",
        "react",
        "sql",
        "git",
        "github",
        "fastapi",
        "django",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pandas",
        "numpy"
    ]

    current_skills = []

    for skill in skill_list:
        if skill in resume_text:
            current_skills.append(skill)

    # Required skills for Frontend + Python Developer
    required_skills = [
        "html",
        "css",
        "javascript",
        "react",
        "git",
        "github",
        "python",
        "sql",
        "fastapi"
    ]

    # Find missing skills
    missing_skills = []

    for skill in required_skills:
        if skill not in current_skills:
            missing_skills.append(skill)

    return {
        "status": "success",
        "profile_id": profile_id,
        "name": profile.name,
        "career_goal": profile.career_goal,
        "current_skills": current_skills,
        "required_skills": required_skills,
        "missing_skills": missing_skills,
        "total_current_skills": len(current_skills),
        "total_missing_skills": len(missing_skills)
    }
    
    # Career Recommendation API
@app.get("/career-recommendation/{profile_id}")
def career_recommendation(
    profile_id: int,
    db: Session = Depends(get_db)
):
    # Find profile
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if profile is None:
        return {
            "status": "error",
            "message": "Profile not found"
        }

    # Check resume
    if not profile.resume_text:
        return {
            "status": "error",
            "message": "Resume text not found. Please upload and extract resume first."
        }

    resume_text = profile.resume_text.lower()

    # Detect skills
    skill_list = [
        "python",
        "c",
        "c++",
        "html",
        "css",
        "javascript",
        "java",
        "data analysis",
        "frontend development",
        "react",
        "sql",
        "git",
        "github",
        "fastapi",
        "django",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pandas",
        "numpy"
    ]

    current_skills = []

    for skill in skill_list:
        if skill in resume_text:
            current_skills.append(skill)

    # Career skill requirements
    career_requirements = {
        "Frontend Developer": [
            "html",
            "css",
            "javascript",
            "react",
            "git",
            "github"
        ],
        "Python Backend Developer": [
            "python",
            "sql",
            "fastapi",
            "git",
            "github"
        ],
        "Full Stack Developer": [
            "html",
            "css",
            "javascript",
            "react",
            "python",
            "sql",
            "fastapi",
            "git",
            "github"
        ],
        "Data Analyst": [
            "python",
            "sql",
            "pandas",
            "numpy",
            "data analysis"
        ]
    }

    recommendations = []

    # Calculate career match
    for career, required_skills in career_requirements.items():

        matched_skills = []

        for skill in required_skills:
            if skill in current_skills:
                matched_skills.append(skill)

        match_percentage = round(
            (len(matched_skills) / len(required_skills)) * 100
        )

        missing_skills = []

        for skill in required_skills:
            if skill not in current_skills:
                missing_skills.append(skill)

        recommendations.append({
            "career": career,
            "match_percentage": match_percentage,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    # Sort careers by highest match
    recommendations.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return {
        "status": "success",
        "profile_id": profile_id,
        "name": profile.name,
        "career_goal": profile.career_goal,
        "current_skills": current_skills,
        "career_recommendations": recommendations
    }
    
    # Learning Roadmap API
@app.get("/learning-roadmap/{profile_id}")
def learning_roadmap(
    profile_id: int,
    db: Session = Depends(get_db)
):
    # Find profile
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if profile is None:
        return {
            "status": "error",
            "message": "Profile not found"
        }

    # Check resume
    if not profile.resume_text:
        return {
            "status": "error",
            "message": "Resume text not found. Please upload and extract resume first."
        }

    resume_text = profile.resume_text.lower()

    # Detect current skills
    skill_list = [
        "python",
        "c",
        "c++",
        "html",
        "css",
        "javascript",
        "java",
        "data analysis",
        "frontend development",
        "react",
        "sql",
        "git",
        "github",
        "fastapi",
        "django",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pandas",
        "numpy"
    ]

    current_skills = []

    for skill in skill_list:
        if skill in resume_text:
            current_skills.append(skill)

    # Required skills for Frontend Developer
    required_skills = [
        "html",
        "css",
        "javascript",
        "react",
        "git",
        "github"
    ]

    # Find missing skills
    missing_skills = []

    for skill in required_skills:
        if skill not in current_skills:
            missing_skills.append(skill)

    # Learning roadmap
    roadmap_data = {
        "react": {
            "priority": "High",
            "duration": "2-3 weeks",
            "topics": [
                "React Components",
                "Props and State",
                "Hooks",
                "React Router",
                "API Integration"
            ],
            "project": "Build a React Portfolio Website"
        },
        "git": {
            "priority": "High",
            "duration": "3-5 days",
            "topics": [
                "Git Basics",
                "Repositories",
                "Commit",
                "Branch",
                "Merge"
            ],
            "project": "Create and manage a Git repository"
        },
        "github": {
            "priority": "Medium",
            "duration": "2-3 days",
            "topics": [
                "GitHub Repository",
                "Push and Pull",
                "README",
                "Issues",
                "Pull Requests"
            ],
            "project": "Upload projects to GitHub"
        }
    }

    roadmap = []

    for skill in missing_skills:
        if skill in roadmap_data:
            roadmap.append({
                "skill": skill,
                "priority": roadmap_data[skill]["priority"],
                "duration": roadmap_data[skill]["duration"],
                "topics": roadmap_data[skill]["topics"],
                "project": roadmap_data[skill]["project"]
            })

    return {
        "status": "success",
        "profile_id": profile_id,
        "name": profile.name,
        "career_goal": profile.career_goal,
        "current_skills": current_skills,
        "missing_skills": missing_skills,
        "learning_roadmap": roadmap
    }
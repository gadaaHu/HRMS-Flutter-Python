import os
import hashlib
import secrets
import uuid
from datetime import date, datetime
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException, Header, File, UploadFile, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, get_db, SessionLocal

# ─── Create Tables ────────────────────────────────────────────────────────────
models.Base.metadata.create_all(bind=engine)

# ─── Create upload directory ──────────────────────────────────────────────────
UPLOAD_DIR = "storage/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ─── App Setup ────────────────────────────────────────────────────────────────
app = FastAPI(title="HRMS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/storage", StaticFiles(directory="storage"), name="storage")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def generate_token() -> str:
    return secrets.token_hex(32)

def require_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> models.User:
    """Validate Bearer token and return authenticated user."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    token = authorization.split(" ", 1)[1]
    user = db.query(models.User).filter(models.User.token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


def seed_initial_data():
    """Create sample data if the database is empty."""
    db = SessionLocal()
    try:
        if db.query(models.User).count() > 0:
            return

        # Create test user
        user = models.User(
            userid="EMP001",
            first_name="John",
            last_name="Doe",
            email="test@test.com",
            password_hash=hash_password("test"),
            phone_number="9876543210",
            work_location="Head Office",
            status="active",
            type="employee",
            token=generate_token()
        )
        db.add(user)
        db.flush()

        # Personal details
        db.add(models.PersonalDetail(
            userid=user.userid,
            dob="1990-08-15",
            gender="Male",
            bio="Software developer with 5 years of experience",
            address="123 Main Street",
            city="Bengaluru",
            state="Karnataka",
            country="India",
            zipcode="560001",
        ))

        # Professional details
        db.add(models.ProfessionalDetail(
            userid=user.userid,
            designation="Software Engineer",
            experience="5 Years",
            skills="Flutter, Python, PostgreSQL",
            joining_date="2020-01-15",
        ))

        # Family details
        db.add(models.FamilyDetail(
            userid=user.userid,
            father_name="Robert Doe",
            mother_name="Mary Doe",
            personal_email="john.personal@gmail.com",
            alternate_contact="9876543211",
            family_address="456 Park Avenue, Bengaluru",
        ))

        # Bank details
        db.add(models.BankDetail(
            userid=user.userid,
            bank_name="State Bank of India",
            account_no="123456789012",
            ifsc_code="SBIN0001234",
            branch_name="MG Road Branch",
            pan_card="ABCDE1234F",
            aadhar_card="123456789012",
        ))

        # Office location
        db.add(models.OfficeLocation(
            name="Head Office",
            latitude="12.9716",
            longitude="77.5946",
            radius_meters=200,
        ))

        # Sample holidays
        holidays = [
            ("New Year",        "2026-01-01", "Thursday"),
            ("Republic Day",    "2026-01-26", "Monday"),
            ("Holi",            "2026-03-14", "Saturday"),
            ("Good Friday",     "2026-04-03", "Friday"),
            ("Independence Day","2026-08-15", "Saturday"),
            ("Gandhi Jayanti",  "2026-10-02", "Friday"),
            ("Diwali",          "2026-10-20", "Tuesday"),
            ("Christmas",       "2026-12-25", "Friday"),
        ]
        for name, d, day in holidays:
            db.add(models.Holiday(name=name, date=d, day=day))

        # Today's attendance seed
        db.add(models.Attendance(
            userid=user.userid,
            date=date.today(),
            intime="09:00",
            outtime="18:00",
            totalhours="09:00",
        ))

        db.commit()
        print("✅ Seed data created. Login: test@test.com / test")
    except Exception as e:
        db.rollback()
        print(f"⚠️  Seed failed (may already exist): {e}")
    finally:
        db.close()


# Run seed on startup
seed_initial_data()


# ─── Pydantic Schemas ─────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str

class AttendanceRequest(BaseModel):
    email: str
    current_address: str
    coordinate: str

class LeaveRequest(BaseModel):
    userid: str
    leave_type: str
    start_date: str
    end_date: str
    reason: Optional[str] = None

class RegularizationRequest(BaseModel):
    userid: str
    date: str
    intime: Optional[str] = None
    outtime: Optional[str] = None
    reason: Optional[str] = None

class ResignationRequest(BaseModel):
    userid: str
    reason: Optional[str] = None
    last_working_day: Optional[str] = None

class DeviceTokenRequest(BaseModel):
    userid: str
    device_token: str
    device_os: Optional[str] = None
    device_name: Optional[str] = None
    os_version: Optional[str] = None

class ProfilePersonalRequest(BaseModel):
    userid: str
    dob: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    address: Optional[str] = None
    address2: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None
    country: Optional[str] = None
    address_type: Optional[str] = None

class ProfileProfessionalRequest(BaseModel):
    userid: str
    designation: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None
    joining_date: Optional[str] = None

class ProfileFamilyRequest(BaseModel):
    userid: str
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    personal_email: Optional[str] = None
    alternate_contact: Optional[str] = None
    family_address: Optional[str] = None

class ProfileBankRequest(BaseModel):
    userid: str
    bank_name: Optional[str] = None
    account_no: Optional[str] = None
    ifsc_code: Optional[str] = None
    branch_name: Optional[str] = None
    bank_address: Optional[str] = None
    pan_card: Optional[str] = None
    aadhar_card: Optional[str] = None


# ─── HEALTH CHECK ─────────────────────────────────────────────────────────────

@app.get("/")
def health_check():
    return {"status": "ok", "message": "HRMS API is running"}


# ─── AUTH ─────────────────────────────────────────────────────────────────────

@app.post("/api/v1/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Refresh token on each login
    user.token = generate_token()
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "status_code": 200,
        "data": {
            "token": user.token,
            "name": f"{user.first_name} {user.last_name}"
        },
        "message": "Login successful"
    }


# ─── USER PROFILE ─────────────────────────────────────────────────────────────

@app.get("/api/v1/get-user")
def get_user(
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.userid == current_user.userid).first()
    pro  = user.professional_detail
    pers = user.personal_detail
    fam  = user.family_detail
    bank = user.bank_detail

    return {
        "success": True,
        "status_code": 200,
        "data": [{
            "id": user.id,
            "userid": user.userid,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "work_location": user.work_location,
            "status": user.status,
            "type": user.type,
            "email_verified_at": user.email_verified_at,
            "created_at": str(user.created_at) if user.created_at else None,
            "updated_at": str(user.updated_at) if user.updated_at else None,
        }],
        "professionalDetails": [{
            "id": pro.id,
            "userid": user.userid,
            "designation": pro.designation,
            "experience": pro.experience,
            "skills": pro.skills,
            "joining_date": pro.joining_date,
            "termination_date": pro.termination_date,
            "termination_reason": pro.termination_reason,
        }] if pro else [],
        "personalDetails": [{
            "id": pers.id,
            "userid": user.userid,
            "src": pers.src,
            "mime_type": pers.mime_type,
            "gender": pers.gender,
            "dob": pers.dob,
            "bio": pers.bio,
            "address": pers.address,
            "address2": pers.address2,
            "state": pers.state,
            "city": pers.city,
            "zipcode": pers.zipcode,
            "country": pers.country,
            "address_type": pers.address_type,
        }] if pers else [],
        "familyDetails": [{
            "id": fam.id,
            "userid": user.userid,
            "father_name": fam.father_name,
            "mother_name": fam.mother_name,
            "personal_email": fam.personal_email,
            "alternate_contact": fam.alternate_contact,
            "family_address": fam.family_address,
        }] if fam else [],
        "bankDetails": [{
            "id": bank.id,
            "userid": user.userid,
            "bank_name": bank.bank_name,
            "account_no": bank.account_no,
            "ifsc_code": bank.ifsc_code,
            "branch_name": bank.branch_name,
            "bank_address": bank.bank_address,
            "pan_card": bank.pan_card,
            "aadhar_card": bank.aadhar_card,
        }] if bank else [],
    }


@app.put("/api/v1/edit-personal")
def edit_personal(
    request: ProfilePersonalRequest,
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    detail = db.query(models.PersonalDetail).filter(
        models.PersonalDetail.userid == current_user.userid
    ).first()
    if not detail:
        detail = models.PersonalDetail(userid=current_user.userid)
        db.add(detail)

    for field, val in request.model_dump(exclude={"userid"}, exclude_none=True).items():
        setattr(detail, field, val)

    db.commit()
    return {"success": True, "message": "Personal details updated successfully"}


@app.put("/api/v1/edit-professional")
def edit_professional(
    request: ProfileProfessionalRequest,
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    detail = db.query(models.ProfessionalDetail).filter(
        models.ProfessionalDetail.userid == current_user.userid
    ).first()
    if not detail:
        detail = models.ProfessionalDetail(userid=current_user.userid)
        db.add(detail)

    for field, val in request.model_dump(exclude={"userid"}, exclude_none=True).items():
        setattr(detail, field, val)

    db.commit()
    return {"success": True, "message": "Professional details updated successfully"}


@app.put("/api/v1/edit-family")
def edit_family(
    request: ProfileFamilyRequest,
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    detail = db.query(models.FamilyDetail).filter(
        models.FamilyDetail.userid == current_user.userid
    ).first()
    if not detail:
        detail = models.FamilyDetail(userid=current_user.userid)
        db.add(detail)

    for field, val in request.model_dump(exclude={"userid"}, exclude_none=True).items():
        setattr(detail, field, val)

    db.commit()
    return {"success": True, "message": "Family details updated successfully"}


@app.put("/api/v1/edit-bank")
def edit_bank(
    request: ProfileBankRequest,
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    detail = db.query(models.BankDetail).filter(
        models.BankDetail.userid == current_user.userid
    ).first()
    if not detail:
        detail = models.BankDetail(userid=current_user.userid)
        db.add(detail)

    for field, val in request.model_dump(exclude={"userid"}, exclude_none=True).items():
        setattr(detail, field, val)

    db.commit()
    return {"success": True, "message": "Bank details updated successfully"}


@app.post("/api/v1/edit-personal/profile-picture")
async def upload_profile_picture(
    src: UploadFile = File(...),
    userid: str = Form(...),
    db: Session = Depends(get_db)
):
    ext = os.path.splitext(src.filename)[1] if src.filename else ".jpg"
    filename = f"{userid}_{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(await src.read())

    detail = db.query(models.PersonalDetail).filter(
        models.PersonalDetail.userid == userid
    ).first()
    if not detail:
        detail = models.PersonalDetail(userid=userid)
        db.add(detail)
    detail.src = filename
    detail.mime_type = src.content_type
    db.commit()

    return {"success": True, "message": "Profile picture updated", "src": filename}


# ─── ATTENDANCE ───────────────────────────────────────────────────────────────

@app.post("/api/v1/user-attendance")
def post_attendance(
    request: AttendanceRequest,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = date.today()
    existing = db.query(models.Attendance).filter(
        models.Attendance.userid == user.userid,
        models.Attendance.date == today
    ).first()

    now_str = datetime.now().strftime("%H:%M")

    if not existing:
        # Punch IN
        record = models.Attendance(
            userid=user.userid,
            date=today,
            intime=now_str,
            current_address=request.current_address,
            coordinate=request.coordinate,
        )
        db.add(record)
        msg = "Punch In successful"
    else:
        # Punch OUT — calculate total hours
        if existing.intime:
            try:
                in_dt  = datetime.strptime(existing.intime, "%H:%M")
                out_dt = datetime.strptime(now_str, "%H:%M")
                diff   = out_dt - in_dt
                hours, rem = divmod(int(diff.total_seconds()), 3600)
                mins = rem // 60
                existing.totalhours = f"{hours:02d}:{mins:02d}"
            except Exception:
                existing.totalhours = None
        existing.outtime = now_str
        msg = "Punch Out successful"

    db.commit()
    return {"success": True, "message": msg}


@app.get("/api/v1/getTodaysAttendance")
def get_todays_attendance(
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    today  = date.today()
    record = db.query(models.Attendance).filter(
        models.Attendance.userid == current_user.userid,
        models.Attendance.date   == today
    ).first()

    if not record:
        return {"success": True, "data": []}

    return {
        "success": True,
        "data": [{
            "intime":          record.intime,
            "outtime":         record.outtime,
            "totalhours":      record.totalhours,
            "current_address": record.current_address,
        }]
    }


@app.get("/api/v1/get-attendance")
def get_attendance(
    month: Optional[str] = Query(None),
    year:  Optional[str] = Query(None),
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    records = db.query(models.Attendance).filter(
        models.Attendance.userid == current_user.userid
    ).all()

    data = [{
        "id":         r.id,
        "userid":     r.userid,
        "date":       str(r.date),
        "intime":     r.intime,
        "outtime":    r.outtime,
        "totalhours": r.totalhours,
    } for r in records]

    return {"success": True, "data": data}


@app.get("/api/v1/getWorkingDays")
def get_working_days(
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    records = db.query(models.Attendance).filter(
        models.Attendance.userid == current_user.userid
    ).all()

    return {
        "success": True,
        "data": {
            "total_working_days": len(records),
            "present_days":       len([r for r in records if r.intime]),
            "absent_days":        0,
        }
    }


# ─── OFFICE LOCATION ──────────────────────────────────────────────────────────

@app.get("/api/v1/get-office")
def get_office(db: Session = Depends(get_db)):
    locations = db.query(models.OfficeLocation).all()
    data = [{
        "latitude":  loc.latitude,
        "longitude": loc.longitude,
        "name":      loc.name,
    } for loc in locations]
    return {"success": True, "data": data}


# ─── LEAVES ───────────────────────────────────────────────────────────────────

@app.get("/api/v1/get-leave-status")
def get_leave_status(
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    leaves   = db.query(models.Leave).filter(models.Leave.userid == current_user.userid).all()
    total    = len(leaves)
    approved = len([l for l in leaves if l.status == "approved"])
    pending  = len([l for l in leaves if l.status == "pending"])
    rejected = len([l for l in leaves if l.status == "rejected"])

    return {
        "success": True,
        "data": [{
            "total_leaves":     total,
            "approved_leaves":  approved,
            "pending_leaves":   pending,
            "rejected_leaves":  rejected,
            "available_leaves": max(0, 20 - approved),
        }]
    }


@app.get("/api/v1/get-leave")
def get_leaves(
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    leaves = db.query(models.Leave).filter(
        models.Leave.userid == current_user.userid
    ).order_by(models.Leave.created_at.desc()).all()

    data = [{
        "id":         l.id,
        "userid":     l.userid,
        "leave_type": l.leave_type,
        "start_date": l.start_date,
        "end_date":   l.end_date,
        "reason":     l.reason,
        "status":     l.status,
        "created_at": str(l.created_at) if l.created_at else None,
    } for l in leaves]

    return {"success": True, "data": data}


@app.post("/api/v1/apply-leave")
def apply_leave(request: LeaveRequest, db: Session = Depends(get_db)):
    leave = models.Leave(
        userid=request.userid,
        leave_type=request.leave_type,
        start_date=request.start_date,
        end_date=request.end_date,
        reason=request.reason,
        status="pending",
    )
    db.add(leave)
    db.commit()
    return {"success": True, "message": "Leave applied successfully"}


# ─── REGULARIZATION ───────────────────────────────────────────────────────────

@app.post("/api/v1/apply-regularization")
def apply_regularization(request: RegularizationRequest, db: Session = Depends(get_db)):
    reg = models.Regularization(
        userid=request.userid,
        date=request.date,
        intime=request.intime,
        outtime=request.outtime,
        reason=request.reason,
        status="pending",
    )
    db.add(reg)
    db.commit()
    return {"success": True, "message": "Regularization request submitted"}


@app.get("/api/v1/get-regularization")
def get_regularization(
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    records = db.query(models.Regularization).filter(
        models.Regularization.userid == current_user.userid
    ).order_by(models.Regularization.created_at.desc()).all()

    data = [{
        "id":      r.id,
        "userid":  r.userid,
        "date":    r.date,
        "intime":  r.intime,
        "outtime": r.outtime,
        "reason":  r.reason,
        "status":  r.status,
    } for r in records]

    return {"success": True, "data": data}


# ─── REIMBURSEMENT ────────────────────────────────────────────────────────────

@app.get("/api/v1/get-reimbursement")
def get_reimbursement(
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    records = db.query(models.Reimbursement).filter(
        models.Reimbursement.userid == current_user.userid
    ).order_by(models.Reimbursement.created_at.desc()).all()

    data = [{
        "id":           r.id,
        "userid":       r.userid,
        "expense_date": r.expense_date,
        "total_amt":    r.total_amt,
        "upi_id":       r.upi_id,
        "status":       r.status,
    } for r in records]

    return {"success": True, "data": data}


@app.post("/api/v1/add-reimbursement")
async def add_reimbursement(
    userid:       str             = Form(...),
    expense_date: str             = Form(...),
    total_amt:    float           = Form(...),
    upi_id:       Optional[str]   = Form(None),
    images:       Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    record = models.Reimbursement(
        userid=userid,
        expense_date=expense_date,
        total_amt=total_amt,
        upi_id=upi_id,
        status="pending",
    )
    db.add(record)
    db.commit()
    return {"success": True, "message": "Reimbursement submitted successfully"}


# ─── RESIGNATION ──────────────────────────────────────────────────────────────

@app.post("/api/v1/create-resign")
def create_resignation(request: ResignationRequest, db: Session = Depends(get_db)):
    resign = models.Resignation(
        userid=request.userid,
        reason=request.reason,
        last_working_day=request.last_working_day,
        status="pending",
    )
    db.add(resign)
    db.commit()
    return {"success": True, "message": "Resignation submitted successfully"}


@app.get("/api/v1/get-resign")
def get_resignation(
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    records = db.query(models.Resignation).filter(
        models.Resignation.userid == current_user.userid
    ).order_by(models.Resignation.created_at.desc()).all()

    data = [{
        "id":               r.id,
        "userid":           r.userid,
        "reason":           r.reason,
        "last_working_day": r.last_working_day,
        "status":           r.status,
        "created_at":       str(r.created_at) if r.created_at else None,
    } for r in records]

    return {"success": True, "data": data}


# ─── HOLIDAYS ─────────────────────────────────────────────────────────────────

@app.get("/api/v1/get-holidays")
def get_holidays(db: Session = Depends(get_db)):
    holidays = db.query(models.Holiday).order_by(models.Holiday.date).all()
    data = [{
        "id":   h.id,
        "name": h.name,
        "date": h.date,
        "day":  h.day,
    } for h in holidays]
    return {"success": True, "data": data}


# ─── NOTIFICATIONS & DEVICE TOKEN ─────────────────────────────────────────────

@app.post("/api/v1/add-user-deviceToken")
def add_device_token(request: DeviceTokenRequest, db: Session = Depends(get_db)):
    existing = db.query(models.DeviceToken).filter(
        models.DeviceToken.userid       == request.userid,
        models.DeviceToken.device_token == request.device_token
    ).first()
    if not existing:
        db.add(models.DeviceToken(
            userid=request.userid,
            device_token=request.device_token,
            device_os=request.device_os,
            device_name=request.device_name,
            os_version=request.os_version,
        ))
        db.commit()
    return {"success": True, "message": "Device token registered"}


@app.get("/api/v1/get-user-notification")
def get_notifications(
    current_user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    notes = db.query(models.Notification).filter(
        models.Notification.userid == current_user.userid
    ).order_by(models.Notification.created_at.desc()).all()

    data = [{
        "id":         n.id,
        "title":      n.title,
        "message":    n.message,
        "is_read":    n.is_read,
        "created_at": str(n.created_at) if n.created_at else None,
    } for n in notes]

    return {"success": True, "data": data}


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

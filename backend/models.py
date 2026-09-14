from sqlalchemy import (
    Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Time, Float, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    phone_number = Column(String, nullable=True)
    work_location = Column(String, nullable=True)
    status = Column(String, default="active")
    type = Column(String, default="employee")
    token = Column(String, nullable=True)
    email_verified_at = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    professional_detail = relationship("ProfessionalDetail", back_populates="user", uselist=False)
    personal_detail = relationship("PersonalDetail", back_populates="user", uselist=False)
    family_detail = relationship("FamilyDetail", back_populates="user", uselist=False)
    bank_detail = relationship("BankDetail", back_populates="user", uselist=False)
    attendances = relationship("Attendance", back_populates="user")
    leaves = relationship("Leave", back_populates="user")
    reimbursements = relationship("Reimbursement", back_populates="user")
    regularizations = relationship("Regularization", back_populates="user")
    resignations = relationship("Resignation", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    device_tokens = relationship("DeviceToken", back_populates="user")


class ProfessionalDetail(Base):
    __tablename__ = "professional_details"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"), unique=True)
    designation = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    skills = Column(String, nullable=True)
    joining_date = Column(String, nullable=True)
    termination_date = Column(String, nullable=True)
    termination_reason = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="professional_detail")


class PersonalDetail(Base):
    __tablename__ = "personal_details"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"), unique=True)
    src = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)
    dob = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    address = Column(String, nullable=True)
    address2 = Column(String, nullable=True)
    state = Column(String, nullable=True)
    city = Column(String, nullable=True)
    zipcode = Column(String, nullable=True)
    country = Column(String, nullable=True)
    address_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="personal_detail")


class FamilyDetail(Base):
    __tablename__ = "family_details"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"), unique=True)
    father_name = Column(String, nullable=True)
    mother_name = Column(String, nullable=True)
    personal_email = Column(String, nullable=True)
    alternate_contact = Column(String, nullable=True)
    family_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="family_detail")


class BankDetail(Base):
    __tablename__ = "bank_details"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"), unique=True)
    bank_name = Column(String, nullable=True)
    account_no = Column(String, nullable=True)
    ifsc_code = Column(String, nullable=True)
    branch_name = Column(String, nullable=True)
    bank_address = Column(String, nullable=True)
    pan_card = Column(String, nullable=True)
    aadhar_card = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="bank_detail")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"))
    date = Column(Date)
    intime = Column(String, nullable=True)
    outtime = Column(String, nullable=True)
    totalhours = Column(String, nullable=True)
    current_address = Column(String, nullable=True)
    coordinate = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="attendances")


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"))
    leave_type = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    reason = Column(Text, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="leaves")


class Regularization(Base):
    __tablename__ = "regularizations"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"))
    date = Column(String)
    intime = Column(String, nullable=True)
    outtime = Column(String, nullable=True)
    reason = Column(Text, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="regularizations")


class Reimbursement(Base):
    __tablename__ = "reimbursements"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"))
    expense_date = Column(String, nullable=True)
    total_amt = Column(Float, nullable=True)
    upi_id = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="reimbursements")


class Resignation(Base):
    __tablename__ = "resignations"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"))
    reason = Column(Text, nullable=True)
    last_working_day = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="resignations")


class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(String)
    day = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"))
    title = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="notifications")


class DeviceToken(Base):
    __tablename__ = "device_tokens"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, ForeignKey("users.userid"))
    device_token = Column(String)
    device_os = Column(String, nullable=True)
    device_name = Column(String, nullable=True)
    os_version = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="device_tokens")


class OfficeLocation(Base):
    __tablename__ = "office_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    latitude = Column(String)
    longitude = Column(String)
    radius_meters = Column(Integer, default=200)

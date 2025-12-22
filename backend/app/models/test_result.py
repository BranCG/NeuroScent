from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class TestResult(Base):
    """Test result model for storing completed tests"""
    
    __tablename__ = "test_results"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    answers = Column(JSON, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", backref="test_results")
    
    def __repr__(self):
        return f"<TestResult {self.id}>"


class OlfactoryProfile(Base):
    """Olfactory profile model generated from test results"""
    
    __tablename__ = "olfactory_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    test_result_id = Column(String(36), ForeignKey("test_results.id", ondelete="CASCADE"))
    
    # Numeric vectors (0.0 - 1.0)
    intensity = Column(Float, nullable=False)
    citrus = Column(Float, default=0.0)
    floral = Column(Float, default=0.0)
    woody = Column(Float, default=0.0)
    sweet = Column(Float, default=0.0)
    spicy = Column(Float, default=0.0)
    green = Column(Float, default=0.0)
    aquatic = Column(Float, default=0.0)
    
    # Contextual data (JSON for SQLite)
    rejected_families = Column(JSON, default=list)
    emotion = Column(String(100))
    time_of_day = Column(JSON, default=list)
    occasions = Column(JSON, default=list)
    season = Column(String(50))
    longevity = Column(Float)
    concentration = Column(String(50))
    reference_perfume = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    test_result = relationship("TestResult", backref="olfactory_profile")
    
    def to_vector(self):
        """Convert profile to vector for similarity calculation"""
        return [
            self.intensity or 0.0,
            self.citrus or 0.0,
            self.floral or 0.0,
            self.woody or 0.0,
            self.sweet or 0.0,
            self.spicy or 0.0,
            self.green or 0.0,
            self.aquatic or 0.0
        ]
    
    def __repr__(self):
        return f"<OlfactoryProfile {self.id}>"

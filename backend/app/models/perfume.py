from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class Perfume(Base):
    """Perfume model for storing perfume information"""
    
    __tablename__ = "perfumes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    image_url = Column(String(500))
    purchase_url = Column(String(500))
    gender = Column(String(20), default="unisex", index=True)  # "male", "female", "unisex"
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Perfume {self.brand} - {self.name}>"


class PerfumeVector(Base):
    """Perfume vector model for olfactory characteristics"""
    
    __tablename__ = "perfume_vectors"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    perfume_id = Column(String(36), ForeignKey("perfumes.id", ondelete="CASCADE"), unique=True)
    
    # Olfactory vectors (0.0 - 1.0)
    intensity = Column(Float, nullable=False)
    citrus = Column(Float, default=0.0)
    floral = Column(Float, default=0.0)
    woody = Column(Float, default=0.0)
    sweet = Column(Float, default=0.0)
    spicy = Column(Float, default=0.0)
    green = Column(Float, default=0.0)
    aquatic = Column(Float, default=0.0)
    
    # Metadata (JSON for SQLite)
    suitable_occasions = Column(JSON, default=list)
    suitable_times = Column(JSON, default=list)
    season = Column(String(50))
    longevity = Column(Float)
    concentration = Column(String(50))
    
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    perfume = relationship("Perfume", backref="vector")
    
    def to_vector(self):
        """Convert perfume characteristics to vector"""
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
        return f"<PerfumeVector for Perfume {self.perfume_id}>"


class AffinityResult(Base):
    """Affinity result model for storing calculated matches"""
    
    __tablename__ = "affinity_results"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = Column(String(36), ForeignKey("olfactory_profiles.id", ondelete="CASCADE"))
    perfume_id = Column(String(36), ForeignKey("perfumes.id", ondelete="CASCADE"))
    affinity_score = Column(Float, nullable=False)
    personalized_description = Column(Text)
    usage_recommendation = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profile = relationship("OlfactoryProfile", backref="affinity_results")
    perfume = relationship("Perfume", backref="affinity_results")
    
    def __repr__(self):
        return f"<AffinityResult {self.affinity_score}%>"

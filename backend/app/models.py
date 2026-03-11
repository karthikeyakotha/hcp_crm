from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Association table for Interaction <-> Material
interaction_material = Table('interaction_material', Base.metadata,
    Column('interaction_id', Integer, ForeignKey('interactions.id')),
    Column('material_id', Integer, ForeignKey('materials.id'))
)

class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialty = Column(String)
    contact_info = Column(String)

    interactions = relationship("Interaction", back_populates="hcp")

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"))
    interaction_type = Column(String) # e.g., Meeting, Call, Email
    date = Column(Date)
    time = Column(Time)
    attendees = Column(String)
    topics_discussed = Column(Text)
    outcomes = Column(Text)
    follow_up_actions = Column(Text)

    hcp = relationship("HCP", back_populates="interactions")
    materials_shared = relationship("Material", secondary=interaction_material, back_populates="interactions")

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String) # Sample, Brochure, Trial, etc.

    interactions = relationship("Interaction", secondary=interaction_material, back_populates="materials_shared")


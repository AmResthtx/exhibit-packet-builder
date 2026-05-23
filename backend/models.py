"""Database models for Exhibit Packet Builder."""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

# Association table for many-to-many relationship between Exhibits and SourceDocuments
exhibit_source_documents = Table(
    'exhibit_source_documents',
    Base.metadata,
    Column('exhibit_id', String, ForeignKey('exhibits.id')),
    Column('document_id', String, ForeignKey('source_documents.id'))
)


class SourceDocument(Base):
    """Source document model."""
    __tablename__ = "source_documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    packet_id = Column(String, ForeignKey('packets.id'), nullable=False)
    original_filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, docx, jpg, etc.
    file_path = Column(String, nullable=False)  # Path on disk
    file_size = Column(Integer, nullable=False)  # in bytes
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    # Extracted metadata
    extracted_date = Column(DateTime, nullable=True)  # Extracted from file
    date_confidence = Column(Float, default=0.0)  # 0.0-1.0 confidence score
    date_source = Column(String, nullable=True)  # "exif", "pdf_metadata", "filename", "ocr", "manual"
    
    # Relationships
    packet = relationship("Packet", back_populates="source_documents")
    exhibits = relationship("Exhibit", secondary=exhibit_source_documents, back_populates="source_documents")
    
    def __repr__(self):
        return f"<SourceDocument {self.original_filename}>"


class Exhibit(Base):
    """Exhibit model."""
    __tablename__ = "exhibits"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    packet_id = Column(String, ForeignKey('packets.id'), nullable=False)
    exhibit_number = Column(String, nullable=False)  # "A", "B", etc. or custom
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    chronological_date = Column(DateTime, nullable=True)  # When this exhibit occurred
    display_order = Column(Integer, nullable=False)  # Order in packet
    
    # Screenshots and content
    screenshot_path = Column(String, nullable=True)  # Path to extracted screenshot
    caption = Column(Text, nullable=True)  # Why this is in the packet
    extracted_text = Column(Text, nullable=True)  # OCR'd text from screenshot
    
    # Legal relevance
    legal_relevance_score = Column(Float, default=0.0)  # Based on applicable laws
    relevant_rules = Column(Text, nullable=True)  # JSON array of applicable rules
    highlighted_sections = Column(Text, nullable=True)  # JSON array of key sections
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    packet = relationship("Packet", back_populates="exhibits")
    source_documents = relationship("SourceDocument", secondary=exhibit_source_documents, back_populates="exhibits")
    
    def __repr__(self):
        return f"<Exhibit {self.exhibit_number}: {self.title}>"


class LegalRule(Base):
    """Legal rule/law model."""
    __tablename__ = "legal_rules"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    state = Column(String, nullable=False)  # "TX", "CA", "FEDERAL", etc.
    category = Column(String, nullable=False)  # "Evidence", "Authentication", "Admissibility", etc.
    rule_name = Column(String, nullable=False)  # e.g., "Rule 801 - Hearsay"
    rule_text = Column(Text, nullable=False)  # Full text of the rule
    keywords = Column(Text, nullable=True)  # JSON array of keywords to detect
    case_types = Column(Text, nullable=True)  # JSON array of applicable case types
    
    # Relationships
    packets = relationship("Packet", secondary="packet_legal_rules", back_populates="legal_rules")
    
    def __repr__(self):
        return f"<LegalRule {self.state} - {self.rule_name}>"


packet_legal_rules = Table(
    'packet_legal_rules',
    Base.metadata,
    Column('packet_id', String, ForeignKey('packets.id')),
    Column('rule_id', String, ForeignKey('legal_rules.id'))
)


class Packet(Base):
    """Exhibit packet model."""
    __tablename__ = "packets"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)  # e.g., "Smith v. Jones - Contract Dispute"
    description = Column(Text, nullable=True)
    case_number = Column(String, nullable=True)
    jurisdiction = Column(String, nullable=True)  # "Texas", "California", etc.
    
    # Processing state
    status = Column(String, default="draft")  # draft, organizing, curating, complete
    
    # Generated outputs
    pdf_path = Column(String, nullable=True)  # Path to generated PDF
    pdf_generated_at = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    source_documents = relationship("SourceDocument", back_populates="packet", cascade="all, delete-orphan")
    exhibits = relationship("Exhibit", back_populates="packet", cascade="all, delete-orphan")
    legal_rules = relationship("LegalRule", secondary=packet_legal_rules, back_populates="packets")
    
    def __repr__(self):
        return f"<Packet {self.name}>"

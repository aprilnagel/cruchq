from datetime import datetime, timezone
from .extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # For default timestamp
from sqlalchemy.ext.mutable import MutableList # For mutable list columns


#Model relationships: create a python-level connection between tables so we can do things like user.role, tour.shows etc.
#Back_populates: Tells SQLAlchemy to populate the relationship in both directions. Each relationship has two sides, Parent and Child. 
#relationship syntax: name = relationship("RelatedModel Name", back_populates="related_model_attribute_name_in_related_model" (the name we give it), cascade="all, delete-orphan")

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state_province = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    continent = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    dob = db.Column(db.Date, nullable=True)
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'), nullable=True)
    pronouns_id = db.Column(db.Integer, db.ForeignKey('pronouns.id'), nullable=True)
    profile_picture_url = db.Column(db.String(255), nullable=True)
    touring_since = db.Column(db.Integer, nullable=True)  # The year the user started working on tours, derived from their earliest tour request or crew assignment
    system_role = db.Column(db.String(50), nullable=False, default='user')  # user, admin, superadmin etc. This is separate from the user roles in case we want to have system-level roles that aren't tied to specific tours or shows.
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    
#----Relationships----  

    gender = relationship("Genders", back_populates="users")
    pronouns = relationship("Pronouns", back_populates="users")
    
    user_roles = relationship("UserRoles", back_populates="user", cascade="all, delete-orphan") 
    user_experience_roles = relationship("UserExperienceRoles", back_populates="user", cascade="all, delete-orphan")
    user_skills = relationship("UserSkills", back_populates="user", cascade="all, delete-orphan")
    user_certifications = relationship("UserCertifications", back_populates="user", cascade="all, delete-orphan")
    user_social_media_links = relationship("UserSocialMediaLinks", back_populates="user", cascade="all, delete-orphan")
    
    tour_crew = relationship("TourCrew", back_populates="user", passive_deletes=True)
    show_crew = relationship("ShowCrew", back_populates="user", passive_deletes=True)
    
    tour_requests = relationship("TourRequests", back_populates="requestor")
    
class Genders(db.Model):
    __tablename__ = 'genders'
    id = db.Column(db.Integer, primary_key=True)
    gender_name = db.Column(db.String(50), nullable=False)
    
#----Relationships----

    users = relationship("Users", back_populates="gender")
    
class Pronouns(db.Model):
    __tablename__ = 'pronouns'
    id = db.Column(db.Integer, primary_key=True)
    pronoun_label = db.Column(db.String(50), nullable=False)
    
 #----Relationships----
    users = relationship("Users", back_populates="pronouns")

class SocialMediaPlatforms(db.Model):
    __tablename__ = 'social_media_platforms'
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(50), nullable=False)
    
#----Relationships----

    user_social_media_links = relationship("UserSocialMediaLinks", back_populates="platform", cascade="all, delete-orphan")

class ExperienceRoles(db.Model):
    __tablename__ = 'experience_roles'
    id = db.Column(db.Integer, primary_key=True)
    ex_role_name = db.Column(db.String(50), nullable=False)
    ex_role_category = db.Column(db.String(50), nullable=False)
    
#----Relationships----

    user_experience_roles = relationship("UserExperienceRoles", back_populates="experience_role")
    tour_crew = relationship("TourCrew", back_populates="experience_role", passive_deletes=True)
    show_crew = relationship("ShowCrew", back_populates="experience_role", passive_deletes=True)
    
class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    
#----Relationships----

    user_roles = relationship("UserRoles", back_populates="role", cascade="all, delete-orphan")
    

class Skills(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(50), nullable=False)
    
#----Relationships----

    user_skills = relationship("UserSkills", back_populates="skill", cascade="all, delete-orphan")

    

class Certifications(db.Model):
    __tablename__ = 'certifications'
    id = db.Column(db.Integer, primary_key=True)
    certification_name = db.Column(db.String(100), nullable=False)
    issuing_organization = db.Column(db.String(100), nullable=False)
    issue_date = db.Column(db.Date, nullable=True)
    expiration_date = db.Column(db.Date, nullable=True)

#----Relationships----

    user_certifications = relationship("UserCertifications", back_populates="certification", cascade="all, delete-orphan")

class TourRequests(db.Model):
    #tours must have started by the time of request, so start_date is required. end_date can be optional since some tours may not have an official end date at the time of request.
    __tablename__ = 'tour_requests'
    id = db.Column(db.Integer, primary_key=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tour_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    headliner_name = db.Column(db.String(255), nullable=False)
    support_artist_names = db.Column(db.String(255), nullable=False)  # will be a + option to add artists
    continent = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
#----Relationships----

    requestor = relationship("Users", back_populates="tour_requests")

    

class Tours(db.Model):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    tour_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    countries = db.Column(MutableList.as_mutable(db.ARRAY(db.String)), nullable=False)  # List of countries
    continent = db.Column(MutableList.as_mutable(db.ARRAY(db.String)), nullable=False)  # List of continents
    year = db.Column(db.Integer, nullable=False) #derived from tour requests
    size = db.Column(db.String(50), nullable=False)  # small, medium, large
    capacity = db.Column(MutableList.as_mutable(db.ARRAY(db.String)), nullable=False)  # List of capacity ranges (e.g., "0-500", "500-2000", "2000+")
    
#----Relationships----

    shows = relationship("Shows", back_populates="tour", cascade="all, delete-orphan")
    tour_crew = relationship("TourCrew", back_populates="tour", cascade="all, delete-orphan")
    tour_artists = relationship("TourArtists", back_populates="tour", cascade="all, delete-orphan")

    

class Shows(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
    show_date = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    
#----Relationships----

    show_crew = relationship("ShowCrew", back_populates="show", cascade="all, delete-orphan")
    venue = relationship("Venues", back_populates="shows")
    
    tour = relationship("Tours", back_populates="shows")



class Venues(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(MutableList.as_mutable(db.ARRAY(db.String)), nullable=True)  # List of states (for US venues) or provinces (for Canadian venues)
    province = db.Column(MutableList.as_mutable(db.ARRAY(db.String)), nullable=True)  # List of provinces (for Canadian venues) or states (for US venues)
    country = db.Column(MutableList.as_mutable(db.ARRAY(db.String)), nullable=False)  # List of countries (for international venues)
    capacity = db.Column(db.Integer, nullable=True)
    
#----Relationships----

    shows = relationship("Shows", back_populates="venue")



#ASSOCIATION TABLES

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    user = relationship("Users", back_populates="user_roles")
    role = relationship("Roles", back_populates="user_roles")

class UserExperienceRoles(db.Model):
    __tablename__ = 'user_experience_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    experience_role_id = db.Column(db.Integer, db.ForeignKey('experience_roles.id'), nullable=False)
    
    user = relationship("Users", back_populates="user_experience_roles")
    experience_role = relationship("ExperienceRoles", back_populates="user_experience_roles")
    
class UserSkills(db.Model):
    __tablename__ = 'user_skills'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    proficiency_level = db.Column(db.Integer, nullable=True)  # Optional proficiency level (e.g., 1-5)
    
    user = relationship("Users", back_populates="user_skills")
    skill = relationship("Skills", back_populates="user_skills")
    
class UserSocialMediaLinks(db.Model):
    __tablename__ = 'user_social_media_links'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('social_media_platforms.id'), nullable=False)
    profile_url = db.Column(db.String(255), nullable=False)
    
    user = relationship("Users", back_populates="user_social_media_links")
    platform = relationship("SocialMediaPlatforms", back_populates="user_social_media_links")
    
class UserCertifications(db.Model):
    __tablename__ = 'user_certifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    certification_id = db.Column(db.Integer, db.ForeignKey('certifications.id'), nullable=False)
    
    user = relationship("Users", back_populates="user_certifications")
    certification = relationship("Certifications", back_populates="user_certifications")
    
class TourCrew(db.Model):
    __tablename__ = 'tour_crew'
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    experience_role_id = db.Column(db.Integer, db.ForeignKey('experience_roles.id'), nullable=False)
    artist_worked_for = db.Column(MutableList.as_mutable(db.ARRAY(db.String)), nullable=True)  # List of artists the crew member has worked for on this tour. Derived from Tour Requests headliner and support artists.
    start_date = db.Column(db.String(255), nullable=False)  # Start date of the crew member's involvement in the tour
    end_date = db.Column(db.String(255), nullable=True)  # End date of the crew member's involvement in the tour (can be null if still active)
    
    tour = relationship("Tours", back_populates="tour_crew")
    user = relationship("Users", back_populates="tour_crew")
    experience_role = relationship("ExperienceRoles", back_populates="tour_crew")
    

class TourArtists(db.Model):
    __tablename__ = 'tour_artists'
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
    artist_name = db.Column(db.String(255), nullable=False)
    artist_role = db.Column(db.Enum('headliner', 'support', name='artist_role'), nullable=False)  # Role of the artist on the tour (e.g., headliner, support)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    tour = relationship("Tours", back_populates="tour_artists")
    

class ShowCrew(db.Model):
    __tablename__ = 'show_crew'
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    experience_role_id = db.Column(db.Integer, db.ForeignKey('experience_roles.id'), nullable=False)
    artist_worked_for = db.Column(MutableList.as_mutable(db.ARRAY(db.String)), nullable=True)  # List of artists the crew member has worked for on this show. Derived from TourArtists headliner and support artists.
    coverage_url = db.Column(db.String(255), nullable=True)  # Optional URL to a news article, blog post, or social media post that mentions the crew member's work on this show
    start_date = db.Column(db.String(255), nullable=False)  # Start date of the crew member's involvement in the show
    end_date = db.Column(db.String(255), nullable=True)  # End date of the crew member's involvement in the show (can be null if still active)
    
    show = relationship("Shows", back_populates="show_crew")
    user = relationship("Users", back_populates="show_crew")
    experience_role = relationship("ExperienceRoles", back_populates="show_crew")
    


    
    
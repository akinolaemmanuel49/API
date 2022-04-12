from sqlalchemy.orm import Session

from api.v1.db.models import user_model, profile_model

from api.v1.schemas import profile_schemas


def create_profile(db: Session, user: user_model.User, profile: profile_schemas.ProfileCreate):
    try:
        db_profile = profile_model.Profile(first_name=profile.first_name, last_name=profile.last_name,
                                           date_of_birth=profile.date_of_birth, profile_type=profile.profile_type, owner_id=user.id)
        db.add(db_profile)
        db.flush()
        db.commit()
        db.refresh(db_profile)
        return db_profile
    except Exception:
        db.rollback()


def get_user_profiles(db: Session, user: user_model.User, skip: int = 0, limit: int = 100):
    try:
        db_profile = db.query(profile_model.Profile).filter(
            profile_model.Profile.owner_id == user.id).order_by(profile_model.Profile.created.desc()).offset(skip).limit(limit).all()
        return db_profile
    except Exception:
        db.rollback()


def update_profile(db: Session, profile_id: int, user: user_model.User, profile: profile_schemas.ProfileUpdate):
    try:
        db_profile = db.query(profile_model.Profile).filter(profile_model.Profile.id == profile_id,
                                                            profile_model.Profile.owner_id == user.id).first()
        db_profile.first_name = profile.first_name
        db_profile.last_name = profile.last_name
        db_profile.date_of_birth = profile.date_of_birth
        db_profile.profile_type = profile.profile_type
        db.add(db_profile)
        db.commit()
        return db_profile
    except Exception:
        db.rollback()


def delete_profile(db: Session, profile_id: int, user: user_model.User):
    try:
        db_profile = db.query(profile_model.Profile).filter(
            profile_model.Profile.id == profile_id, profile_model.Profile.owner_id == user.id).first()
        db.delete(db_profile)
        db.commit()
        return db_profile
    except Exception:
        db.rollback()

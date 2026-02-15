"""Two-Factor Authentication (2FA) service."""

from datetime import datetime, timedelta
from typing import Optional
import pyotp
import qrcode
from io import BytesIO
import base64
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dario_app.database import Base


class TwoFactorAuth(Base):
    """2FA configuration model."""
    
    __tablename__ = "two_factor_auth"
    
    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, unique=True, nullable=False, index=True)
    organization_id: int = Column(Integer, nullable=False, index=True)
    
    # TOTP secret (encrypted in production)
    secret: str = Column(String(32), nullable=False)
    
    # Backup codes (encrypted in production)
    backup_codes: str = Column(String(500), nullable=True)
    
    # Status
    is_enabled: bool = Column(Boolean, default=False, nullable=False)
    verified_at: datetime = Column(DateTime, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_used: datetime = Column(DateTime, nullable=True)


class TwoFactorService:
    """Enterprise 2FA service."""
    
    @staticmethod
    def generate_secret() -> str:
        """Generate TOTP secret."""
        return pyotp.random_base32()
    
    @staticmethod
    def generate_backup_codes(count: int = 10) -> list[str]:
        """Generate backup codes."""
        import secrets
        return [
            f"{secrets.randbelow(100000000):08d}"
            for _ in range(count)
        ]
    
    @staticmethod
    def get_provisioning_uri(
        secret: str,
        user_email: str,
        issuer: str = "OmniERP"
    ) -> str:
        """Get provisioning URI for QR code."""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=user_email,
            issuer_name=issuer
        )
    
    @staticmethod
    def generate_qr_code(provisioning_uri: str) -> str:
        """Generate QR code as base64 image."""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        
        return base64.b64encode(buffered.getvalue()).decode()
    
    @staticmethod
    def verify_token(secret: str, token: str) -> bool:
        """Verify TOTP token."""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)  # Allow 30s window
    
    @staticmethod
    async def setup_2fa(
        db: AsyncSession,
        user_id: int,
        organization_id: int,
        user_email: str
    ) -> dict:
        """Setup 2FA for user."""
        # Generate secret and backup codes
        secret = TwoFactorService.generate_secret()
        backup_codes = TwoFactorService.generate_backup_codes()
        
        # Create or update 2FA record
        query = select(TwoFactorAuth).where(TwoFactorAuth.user_id == user_id)
        result = await db.execute(query)
        tfa = result.scalar_one_or_none()
        
        if tfa:
            tfa.secret = secret
            tfa.backup_codes = ",".join(backup_codes)
            tfa.is_enabled = False  # Reset until verified
        else:
            tfa = TwoFactorAuth(
                user_id=user_id,
                organization_id=organization_id,
                secret=secret,
                backup_codes=",".join(backup_codes),
                is_enabled=False
            )
            db.add(tfa)
        
        await db.commit()
        
        # Generate QR code
        provisioning_uri = TwoFactorService.get_provisioning_uri(secret, user_email)
        qr_code = TwoFactorService.generate_qr_code(provisioning_uri)
        
        return {
            "secret": secret,
            "qr_code": qr_code,
            "backup_codes": backup_codes,
            "provisioning_uri": provisioning_uri
        }
    
    @staticmethod
    async def enable_2fa(
        db: AsyncSession,
        user_id: int,
        verification_token: str
    ) -> bool:
        """Enable 2FA after verification."""
        query = select(TwoFactorAuth).where(TwoFactorAuth.user_id == user_id)
        result = await db.execute(query)
        tfa = result.scalar_one_or_none()
        
        if not tfa:
            return False
        
        # Verify token
        if TwoFactorService.verify_token(tfa.secret, verification_token):
            tfa.is_enabled = True
            tfa.verified_at = datetime.utcnow()
            await db.commit()
            return True
        
        return False
    
    @staticmethod
    async def verify_2fa(
        db: AsyncSession,
        user_id: int,
        token: str
    ) -> bool:
        """Verify 2FA token for login."""
        query = select(TwoFactorAuth).where(
            TwoFactorAuth.user_id == user_id,
            TwoFactorAuth.is_enabled == True
        )
        result = await db.execute(query)
        tfa = result.scalar_one_or_none()
        
        if not tfa:
            return False
        
        # Try TOTP token
        if TwoFactorService.verify_token(tfa.secret, token):
            tfa.last_used = datetime.utcnow()
            await db.commit()
            return True
        
        # Try backup codes
        backup_codes = tfa.backup_codes.split(",") if tfa.backup_codes else []
        if token in backup_codes:
            # Remove used backup code
            backup_codes.remove(token)
            tfa.backup_codes = ",".join(backup_codes)
            tfa.last_used = datetime.utcnow()
            await db.commit()
            return True
        
        return False
    
    @staticmethod
    async def disable_2fa(
        db: AsyncSession,
        user_id: int
    ) -> bool:
        """Disable 2FA for user."""
        query = select(TwoFactorAuth).where(TwoFactorAuth.user_id == user_id)
        result = await db.execute(query)
        tfa = result.scalar_one_or_none()
        
        if tfa:
            tfa.is_enabled = False
            await db.commit()
            return True
        
        return False
    
    @staticmethod
    async def is_2fa_enabled(
        db: AsyncSession,
        user_id: int
    ) -> bool:
        """Check if 2FA is enabled for user."""
        query = select(TwoFactorAuth).where(
            TwoFactorAuth.user_id == user_id,
            TwoFactorAuth.is_enabled == True
        )
        result = await db.execute(query)
        return result.scalar_one_or_none() is not None

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Authentication
    is_verified BOOLEAN DEFAULT FALSE,  -- Email verification flag
    verification_token TEXT UNIQUE,  -- Token for email verification
    reset_token TEXT UNIQUE,  -- Token for password reset

    -- OAuth Fields (for Google, Facebook login)
    provider VARCHAR(50),  -- e.g., 'google', 'facebook'
    provider_id VARCHAR(255) UNIQUE,  -- OAuth user ID

    -- Role Management
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'admin')),

    -- Security & Tracking
    last_login TIMESTAMP,
    failed_attempts INT DEFAULT 0,  -- Failed login attempts
    locked_until TIMESTAMP  -- Account lockout for security
);

-- Trigger to update the `updated_at` column for users
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
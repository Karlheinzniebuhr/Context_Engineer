-- Sample data for development and testing
-- Run this after initial schema migration

-- Additional sample users
INSERT INTO users (name, email) VALUES 
    ('Alice Cooper', 'alice@example.com'),
    ('Charlie Brown', 'charlie@example.com'),
    ('Diana Prince', 'diana@example.com'),
    ('Edward Norton', 'edward@example.com'),
    ('Fiona Apple', 'fiona@example.com');

-- Additional sample metrics
INSERT INTO metrics (user_id, name, value, metadata) VALUES 
    (4, 'page_views', 1850.00, '{"source": "organic", "device": "desktop"}'),
    (4, 'session_duration', 42.15, '{"bounce_rate": 0.25}'),
    (4, 'conversion_rate', 3.45, '{"campaign": "summer_sale"}'),
    (5, 'page_views', 920.00, '{"source": "social", "device": "mobile"}'),
    (5, 'session_duration', 28.90, '{"bounce_rate": 0.45}'),
    (5, 'conversion_rate', 2.10, '{"campaign": "winter_promo"}'),
    (6, 'page_views', 3200.00, '{"source": "direct", "device": "desktop"}'),
    (6, 'session_duration', 65.80, '{"bounce_rate": 0.15}'),
    (6, 'conversion_rate', 4.75, '{"campaign": "loyalty_program"}'),
    (7, 'page_views', 1560.00, '{"source": "referral", "device": "tablet"}'),
    (7, 'session_duration', 48.30, '{"bounce_rate": 0.30}'),
    (8, 'page_views', 780.00, '{"source": "email", "device": "mobile"}'),
    (8, 'session_duration', 35.20, '{"bounce_rate": 0.55}');

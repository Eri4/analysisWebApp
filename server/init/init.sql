-- We create tables first
CREATE TABLE campaigns (
                           id SERIAL PRIMARY KEY,
                           campaign_name VARCHAR(100) NOT NULL,
                           platform VARCHAR(50) NOT NULL,
                           region VARCHAR(50) NOT NULL,
                           date DATE NOT NULL,
                           impressions INTEGER NOT NULL,
                           clicks INTEGER NOT NULL,
                           conversions INTEGER NOT NULL,
                           spend DECIMAL(10, 2) NOT NULL,
                           ctr DECIMAL(10, 4) GENERATED ALWAYS AS (CASE WHEN impressions > 0 THEN clicks::decimal / impressions ELSE 0 END) STORED,
    cpc DECIMAL(10, 4) GENERATED ALWAYS AS (CASE WHEN clicks > 0 THEN spend / clicks ELSE 0 END) STORED,
    cpa DECIMAL(10, 4) GENERATED ALWAYS AS (CASE WHEN conversions > 0 THEN spend / conversions ELSE 0 END) STORED,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analyses (
                          id SERIAL PRIMARY KEY,
                          type VARCHAR(50) NOT NULL,
                          metric VARCHAR(50) NOT NULL,
                          description TEXT NOT NULL,
                          severity VARCHAR(20) NOT NULL,
                          value DECIMAL(10, 4),
                          expected_value DECIMAL(10, 4),
                          date_range_start DATE,
                          date_range_end DATE,
                          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                          notified BOOLEAN DEFAULT FALSE
);

CREATE TABLE recommendations (
                                 id SERIAL PRIMARY KEY,
                                 analysis_id INTEGER REFERENCES analyses(id),
                                 content TEXT NOT NULL,
                                 created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
                               id SERIAL PRIMARY KEY,
                               analysis_id INTEGER REFERENCES analyses(id),
                               recipient VARCHAR(100) NOT NULL,
                               subject VARCHAR(200) NOT NULL,
                               content TEXT NOT NULL,
                               sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert data from Facebook Ads Dataset (this is just fake data)

-- Campaign 1: Retargeting Campaign
INSERT INTO campaigns (campaign_name, platform, region, date, impressions, clicks, conversions, spend)
VALUES
-- North America
('Retargeting Campaign', 'Facebook Ads', 'North America', '2025-05-01', 12560, 325, 15, 145.67),
('Retargeting Campaign', 'Facebook Ads', 'North America', '2025-05-02', 13450, 356, 18, 152.34),
('Retargeting Campaign', 'Facebook Ads', 'North America', '2025-05-03', 14200, 378, 19, 160.78),
('Retargeting Campaign', 'Facebook Ads', 'North America', '2025-05-04', 11890, 301, 14, 139.45),
('Retargeting Campaign', 'Facebook Ads', 'North America', '2025-05-05', 12780, 336, 16, 148.90),
('Retargeting Campaign', 'Facebook Ads', 'North America', '2025-05-06', 13567, 365, 17, 155.23),
('Retargeting Campaign', 'Facebook Ads', 'North America', '2025-05-07', 14356, 392, 20, 165.78),
('Retargeting Campaign', 'Facebook Ads', 'North America', '2025-05-08', 13890, 376, 19, 158.67),
('Retargeting Campaign', 'Facebook Ads', 'North America', '2025-05-09', 12980, 342, 17, 150.34),
('Retargeting Campaign', 'Facebook Ads', 'North America', '2025-05-10', 13120, 348, 17, 152.67),
-- Europe
('Retargeting Campaign', 'Facebook Ads', 'Europe', '2025-05-01', 10230, 267, 11, 125.45),
('Retargeting Campaign', 'Facebook Ads', 'Europe', '2025-05-02', 11456, 289, 12, 132.67),
('Retargeting Campaign', 'Facebook Ads', 'Europe', '2025-05-03', 12345, 312, 14, 142.34),
('Retargeting Campaign', 'Facebook Ads', 'Europe', '2025-05-04', 9876, 251, 10, 118.90),
('Retargeting Campaign', 'Facebook Ads', 'Europe', '2025-05-05', 10987, 278, 12, 130.56),
('Retargeting Campaign', 'Facebook Ads', 'Europe', '2025-05-06', 11234, 291, 13, 135.67),
('Retargeting Campaign', 'Facebook Ads', 'Europe', '2025-05-07', 12098, 315, 15, 145.23),
('Retargeting Campaign', 'Facebook Ads', 'Europe', '2025-05-08', 11567, 298, 14, 138.90),
('Retargeting Campaign', 'Facebook Ads', 'Europe', '2025-05-09', 10789, 276, 12, 129.45),
('Retargeting Campaign', 'Facebook Ads', 'Europe', '2025-05-10', 10987, 284, 13, 132.67);

-- Campaign 2: New Customer Acquisition
INSERT INTO campaigns (campaign_name, platform, region, date, impressions, clicks, conversions, spend)
VALUES
-- North America
('New Customer Acquisition', 'Google Ads', 'North America', '2025-05-01', 25670, 587, 23, 234.56),
('New Customer Acquisition', 'Google Ads', 'North America', '2025-05-02', 27890, 623, 25, 248.90),
('New Customer Acquisition', 'Google Ads', 'North America', '2025-05-03', 29450, 678, 28, 265.34),
('New Customer Acquisition', 'Google Ads', 'North America', '2025-05-04', 24560, 542, 21, 223.67),
('New Customer Acquisition', 'Google Ads', 'North America', '2025-05-05', 26780, 598, 24, 241.45),
('New Customer Acquisition', 'Google Ads', 'North America', '2025-05-06', 28340, 643, 26, 256.78),
('New Customer Acquisition', 'Google Ads', 'North America', '2025-05-07', 30120, 698, 29, 273.90),
('New Customer Acquisition', 'Google Ads', 'North America', '2025-05-08', 28760, 657, 27, 262.34),
('New Customer Acquisition', 'Google Ads', 'North America', '2025-05-09', 27450, 621, 25, 249.67),
('New Customer Acquisition', 'Google Ads', 'North America', '2025-05-10', 27890, 632, 26, 253.45),
-- Asia
('New Customer Acquisition', 'Google Ads', 'Asia', '2025-05-01', 18970, 378, 12, 189.45),
('New Customer Acquisition', 'Google Ads', 'Asia', '2025-05-02', 20340, 412, 14, 201.67),
('New Customer Acquisition', 'Google Ads', 'Asia', '2025-05-03', 21780, 445, 15, 215.23),
('New Customer Acquisition', 'Google Ads', 'Asia', '2025-05-04', 17890, 352, 11, 178.90),
('New Customer Acquisition', 'Google Ads', 'Asia', '2025-05-05', 19450, 389, 13, 192.34),
('New Customer Acquisition', 'Google Ads', 'Asia', '2025-05-06', 20670, 421, 14, 204.56),
('New Customer Acquisition', 'Google Ads', 'Asia', '2025-05-07', 22340, 458, 16, 220.67),
('New Customer Acquisition', 'Google Ads', 'Asia', '2025-05-08', 21230, 432, 15, 210.45),
('New Customer Acquisition', 'Google Ads', 'Asia', '2025-05-09', 20120, 406, 14, 199.78),
('New Customer Acquisition', 'Google Ads', 'Asia', '2025-05-10', 20450, 415, 14, 203.23);

-- Campaign 3: Brand Awareness
INSERT INTO campaigns (campaign_name, platform, region, date, impressions, clicks, conversions, spend)
VALUES
-- Global campaign
('Brand Awareness', 'Instagram Ads', 'North America', '2025-05-01', 35670, 723, 18, 287.45),
('Brand Awareness', 'Instagram Ads', 'North America', '2025-05-02', 38450, 784, 20, 305.67),
('Brand Awareness', 'Instagram Ads', 'North America', '2025-05-03', 41230, 845, 22, 323.90),
('Brand Awareness', 'Instagram Ads', 'North America', '2025-05-04', 34560, 701, 17, 278.34),
('Brand Awareness', 'Instagram Ads', 'North America', '2025-05-05', 37340, 761, 19, 296.56),
('Brand Awareness', 'Instagram Ads', 'North America', '2025-05-06', 39780, 812, 21, 314.78),
('Brand Awareness', 'Instagram Ads', 'North America', '2025-05-07', 42340, 867, 23, 332.23),
('Brand Awareness', 'Instagram Ads', 'North America', '2025-05-08', 40120, 821, 21, 318.90),
('Brand Awareness', 'Instagram Ads', 'North America', '2025-05-09', 38450, 785, 20, 305.45),
('Brand Awareness', 'Instagram Ads', 'North America', '2025-05-10', 39120, 798, 20, 309.67);

-- Add some anomalies for our analysis to detect

-- Anomaly 1: Sudden drop in CTR for Retargeting Campaign in Europe
UPDATE campaigns
SET
    impressions = impressions * 1.2,
    clicks = floor(clicks * 0.4)
WHERE
    campaign_name = 'Retargeting Campaign' AND
    platform = 'Facebook Ads' AND
    region = 'Europe' AND
    date = '2025-05-06';

-- Anomaly 2: Unusually high CPA for New Customer Acquisition in Asia
UPDATE campaigns
SET
    spend = spend * 1.8,
    conversions = floor(conversions * 0.6)
WHERE
    campaign_name = 'New Customer Acquisition' AND
    platform = 'Google Ads' AND
    region = 'Asia' AND
    date = '2025-05-08';

-- Anomaly 3: Sudden improvement in conversion rate for Brand Awareness campaign
UPDATE campaigns
SET
    conversions = conversions * 3
WHERE
    campaign_name = 'Brand Awareness' AND
    platform = 'Instagram Ads' AND
    region = 'North America' AND
    date = '2025-05-07';
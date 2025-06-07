-- database: :memory:
ALTER TABLE skill AUTO_INCREMENT = 1;
ALTER TABLE opportunity AUTO_INCREMENT = 1;
ALTER TABLE job_opportunity AUTO_INCREMENT = 1;
ALTER TABLE volunteer_opportunity AUTO_INCREMENT = 1;
ALTER TABLE opportunity_day AUTO_INCREMENT = 1;

-- Insert unique skills into the skill table
INSERT INTO skill (name) VALUES
('Advocacy'),
('Agriculture'),
('Business Development'),
('Business Promotion'),
('Campaign Management'),
('Caregiving'),
('Community Development'),
('Community Engagement'),
('Community Outreach'),
('Community Support'),
('Conflict Resolution'),
('Counseling'),
('Cultural Preservation'),
('Data Analysis'),
('Data Collection'),
('Documentation'),
('Education'),
('Emergency Response'),
('Environmental Education'),
('Environmental Science'),
('Environmental Sustainability'),
('Event Planning'),
('Facilitation'),
('Health Education'),
('Healthcare'),
('Healthcare Systems'),
('International Relations'),
('Legal Advocacy'),
('Legal Analysis'),
('Logistics'),
('Media Production'),
('Medical Training'),
('Mental Health'),
('Mental Health Advocacy'),
('Observation'),
('Policy Analysis'),
('Program Management'),
('Project Management'),
('Public Engagement'),
('Public Health'),
('Public Speaking'),
('Research'),
('Social Media'),
('Strategic Planning'),
('Training'),
('Youth Empowerment'),
('Youth Engagement'),
('Mediation');

-- Insert opportunities into the opportunity table
INSERT INTO opportunity (organization_id, title, description, location, latitude, longitude, start_date, end_date, status, image_url, application_link, contact_email, opportunity_type, is_deleted) VALUES
(1, 'Emergency Medical Technician', 'Provide critical medical support in emergency situations across Palestinian communities, including first aid and patient transport.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-03-01', '2024-12-31', 'OPEN', 'work.png', 'https://palestinercs.org/careers', 'info@palestinercs.org', 'JOB', FALSE),
(1, 'Community Health Outreach Volunteer', 'Assist in organizing health awareness campaigns and basic health screenings in local communities.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-06-01', '2024-09-30', 'OPEN', 'vol.png', 'https://palestinercs.org/volunteer', 'info@palestinercs.org', 'VOLUNTEER', FALSE),
(2, 'Education Program Coordinator', 'Design and implement educational programs to enhance learning opportunities for Palestinian youth.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-04-01', '2024-12-31', 'OPEN', 'work.png', 'https://taawon.org/careers', 'contact@taawon.org', 'JOB', FALSE),
(2, 'Cultural Event Volunteer', 'Support the organization of cultural festivals to preserve Palestinian heritage.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-07-01', '2024-10-31', 'OPEN', 'vol.png', 'https://taawon.org/volunteer', 'contact@taawon.org', 'VOLUNTEER', FALSE),
(3, 'Healthcare Systems Analyst', 'Analyze and improve healthcare delivery systems in Gaza’s medical facilities.', 'Gaza, Palestine', 31.5017, 34.4668, '2024-02-01', '2024-11-30', 'OPEN', 'work.png', 'https://map.org.uk/careers', 'info@map.org.uk', 'JOB', FALSE),
(3, 'Medical Supplies Distribution Volunteer', 'Assist in distributing medical supplies to clinics and hospitals in Gaza.', 'Gaza, Palestine', 31.5017, 34.4668, '2024-05-01', '2024-08-31', 'OPEN', 'vol.png', 'https://map.org.uk/volunteer', 'info@map.org.uk', 'VOLUNTEER', FALSE),
(4, 'Environmental Research Scientist', 'Conduct research on sustainable agricultural practices and water management.', 'Bethlehem, Palestine', 31.7054, 35.1937, '2024-03-15', '2024-12-15', 'OPEN', 'work.png', 'https://arij.org/careers', 'info@arij.org', 'JOB', FALSE),
(4, 'Community Gardening Volunteer', 'Support local communities in developing sustainable community gardens.', 'Bethlehem, Palestine', 31.7054, 35.1937, '2024-06-15', '2024-09-15', 'OPEN', 'vol.png', 'https://arij.org/volunteer', 'info@arij.org', 'VOLUNTEER', FALSE),
(5, 'Public Policy Advocate', 'Develop campaigns to promote democracy and human rights in Palestine.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-04-01', '2024-12-31', 'OPEN', 'work.png', 'https://miftah.org/careers', 'info@miftah.org', 'JOB', FALSE),
(5, 'Democracy Workshop Facilitator', 'Facilitate workshops to educate communities on democratic principles.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-07-01', '2024-10-31', 'OPEN', 'vol.png', 'https://miftah.org/volunteer', 'info@miftah.org', 'VOLUNTEER', FALSE),
(6, 'Human Rights Researcher', 'Document and report on human rights violations in the Occupied Palestinian Territories.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-02-15', '2024-11-30', 'OPEN', 'work.png', 'https://alhaq.org/careers', 'info@alhaq.org', 'JOB', FALSE),
(6, 'Community Human Rights Monitor', 'AssistKid in monitoring and reporting human rights issues in local communities.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-05-15', '2024-08-31', 'OPEN', 'vol.png', 'https://alhaq.org/volunteer', 'info@alhaq.org', 'VOLUNTEER', FALSE),
(7, 'Youth Program Coordinator', 'Develop and manage programs to empower Palestinian youth through media and community service.', 'Beit Sahour, Palestine', 31.7010, 35.2257, '2024-03-01', '2024-12-31', 'OPEN', 'work.png', 'https://pcr.ps/careers', 'info@pcr.ps', 'JOB', FALSE),
(7, 'Media Campaign Volunteer', 'Support the creation of media content to promote community initiatives.', 'Beit Sahour, Palestine', 31.7010, 35.2257, '2024-06-01', '2024-09-30', 'OPEN', 'vol.png', 'https://pcr.ps/volunteer', 'info@pcr.ps', 'VOLUNTEER', FALSE),
(8, 'Community Health Worker', 'Provide healthcare and support services to elderly and vulnerable populations.', 'Bethlehem, Palestine', 31.7054, 35.1937, '2024-04-01', '2024-12-31', 'OPEN', 'work.png', 'https://diyar.ps/careers', 'info@diyar.ps', 'JOB', FALSE),
(8, 'Elderly Care Volunteer', 'Assist in organizing activities and support for elderly community members.', 'Bethlehem, Palestine', 31.7054, 35.1937, '2024-07-01', '2024-10-31', 'OPEN', 'vol.png', 'https://diyar.ps/volunteer', 'info@diyar.ps', 'VOLUNTEER', FALSE),
(9, 'Nonviolence Training Specialist', 'Develop and deliver training programs on nonviolence for youth and women.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-03-15', '2024-12-15', 'OPEN', 'work.png', 'https://mendonline.org/careers', 'info@mendonline.org', 'JOB', FALSE),
(9, 'Youth Empowerment Volunteer', 'Support workshops to empower youth through nonviolence education.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-06-15', '2024-09-15', 'OPEN', 'vol.png', 'https://mendonline.org/volunteer', 'info@mendonline.org', 'VOLUNTEER', FALSE),
(10, 'Ecotourism Project Manager', 'Lead projects to promote ecotourism and environmental sustainability in Palestine.', 'Jericho, Palestine', 31.8611, 35.4599, '2024-02-01', '2024-11-30', 'OPEN', 'work.png', 'https://wedo-pal.org/careers', 'info@wedo-pal.org', 'JOB', FALSE),
(10, 'Environmental Awareness Volunteer', 'Assist in campaigns to raise awareness about environmental protection.', 'Jericho, Palestine', 31.8611, 35.4599, '2024-05-01', '2024-08-31', 'OPEN', 'vol.png', 'https://wedo-pal.org/volunteer', 'info@wedo-pal.org', 'VOLUNTEER', FALSE),
(11, 'Medical Education Coordinator', 'Develop medical education programs for healthcare professionals in Palestine.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-04-01', '2024-12-31', 'OPEN', 'work.png', 'https://pamausa.org/careers', 'info@pamausa.org', 'JOB', FALSE),
(11, 'Health Clinic Volunteer', 'Support medical clinics by assisting with patient intake and basic health checks.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-07-01', '2024-10-31', 'OPEN', 'vol.png', 'https://pamausa.org/volunteer', 'info@pamausa.org', 'VOLUNTEER', FALSE),
(12, 'Legal Advocate for Prisoners', 'Provide legal support and advocacy for Palestinian prisoners.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-03-01', '2024-12-31', 'OPEN', 'work.png', 'https://addameer.org/careers', 'info@addameer.org', 'JOB', FALSE),
(12, 'Prisoner Support Volunteer', 'Assist in organizing support programs for families of prisoners.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-06-01', '2024-09-30', 'OPEN', 'vol.png', 'https://addameer.org/volunteer', 'info@addameer.org', 'VOLUNTEER', FALSE),
(13, 'Policy Analyst', 'Conduct research and analysis to support Palestinian human rights advocacy.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-02-15', '2024-11-30', 'OPEN', 'work.png', 'https://al-shabaka.org/careers', 'info@al-shabaka.org', 'JOB', FALSE),
(13, 'Public Debate Volunteer', 'Support the organization of public debates on Palestinian rights.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-05-15', '2024-08-31', 'OPEN', 'vol.png', 'https://al-shabaka.org/volunteer', 'info@al-shabaka.org', 'VOLUNTEER', FALSE),
(14, 'Youth Leadership Trainer', 'Develop and deliver leadership training programs for Palestinian youth.', 'Gaza, Palestine', 31.5017, 34.4668, '2024-04-01', '2024-12-31', 'OPEN', 'work.png', 'https://healpalestine.org/careers', 'info@healpalestine.org', 'JOB', FALSE),
(14, 'Health Education Volunteer', 'Assist in delivering health education workshops for youth in Gaza.', 'Gaza, Palestine', 31.5017, 34.4668, '2024-07-01', '2024-10-31', 'OPEN', 'vol.png', 'https://healpalestine.org/volunteer', 'info@healpalestine.org', 'VOLUNTEER', FALSE),
(15, 'Mediation Specialist', 'Facilitate conflict resolution and mediation programs in Palestinian communities.', 'Bethlehem, Palestine', 31.7054, 35.1937, '2024-03-01', '2024-12-31', 'OPEN', 'work.png', 'https://wiam.ps/careers', 'info@wiam.ps', 'JOB', FALSE),
(15, 'Nonviolence Training Volunteer', 'Support nonviolence training workshops for community members.', 'Bethlehem, Palestine', 31.7054, 35.1937, '2024-06-01', '2024-09-30', 'OPEN', 'vol.png', 'https://wiam.ps/volunteer', 'info@wiam.ps', 'VOLUNTEER', FALSE),
(16, 'Industrial Development Consultant', 'Support the growth of Palestinian industries through strategic planning and consultation.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-02-01', '2024-11-30', 'OPEN', 'work.png', 'https://pfi.ps/careers', 'info@pfi.ps', 'JOB', FALSE),
(16, 'Industry Outreach Volunteer', 'Assist in promoting industrial development initiatives to local businesses.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-05-01', '2024-08-31', 'OPEN', 'vol.png', 'https://pfi.ps/volunteer', 'info@pfi.ps', 'VOLUNTEER', FALSE),
(17, 'Mental Health Counselor', 'Provide psychological support and counseling services to individuals in Gaza.', 'Gaza, Palestine', 31.5017, 34.4668, '2024-04-01', '2024-12-31', 'OPEN', 'work.png', 'https://hakini.ps/careers', 'info@hakini.ps', 'JOB', FALSE),
(17, 'Mental Health Awareness Volunteer', 'Support campaigns to raise awareness about mental health in Gaza.', 'Gaza, Palestine', 31.5017, 34.4668, '2024-07-01', '2024-10-31', 'OPEN', 'vol.png', 'https://hakini.ps/volunteer', 'info@hakini.ps', 'VOLUNTEER', FALSE),
(18, 'Community Development Officer', 'Lead initiatives to support socio-economic and cultural development in Palestinian communities.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-03-15', '2024-12-15', 'OPEN', 'work.png', 'https://upaconnect.org/careers', 'info@upaconnect.org', 'JOB', FALSE),
(18, 'Cultural Preservation Volunteer', 'Assist in programs to preserve Palestinian cultural heritage.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-06-15', '2024-09-15', 'OPEN', 'vol.png', 'https://upaconnect.org/volunteer', 'info@upaconnect.org', 'VOLUNTEER', FALSE),
(19, 'Advocacy Campaign Manager', 'Lead campaigns to promote the BDS movement for Palestinian rights.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-02-01', '2024-11-30', 'OPEN', 'work.png', 'https://bdsmovement.net/careers', 'info@bdsmovement.net', 'JOB', FALSE),
(19, 'BDS Campaign Volunteer', 'Support grassroots campaigns to promote the BDS movement.', 'Ramallah, Palestine', 31.9038, 35.2034, '2024-05-01', '2024-08-31', 'OPEN', 'vol.png', 'https://bdsmovement.net/volunteer', 'info@bdsmovement.net', 'VOLUNTEER', FALSE),
(20, 'International Affairs Researcher', 'Conduct research on Palestinian issues in international contexts.', 'Jerusalem, Palestine', 31.7683, 35.2137, '2024-04-01', '2024-12-31', 'OPEN', 'work.png', 'https://passia.org/careers', 'info@passia.org', 'JOB', FALSE),
(20, 'Research Assistant Volunteer', 'Assist in collecting data and preparing reports on Palestinian issues.', 'Jerusalem, Palestine', 31.7683, 35.2137, '2024-07-01', '2024-10-31', 'OPEN', 'vol.png', 'https://passia.org/volunteer', 'info@passia.org', 'VOLUNTEER', FALSE);

-- Insert job opportunities into the job_opportunity table
INSERT INTO job_opportunity (opportunity_id, required_points) VALUES
(1, 500),
(3, 600),
(5, 550),
(7, 600),
(9, 650),
(11, 600),
(13, 550),
(15, 500),
(17, 600),
(19, 650),
(21, 550),
(23, 600),
(25, 650),
(27, 550),
(29, 600),
(31, 650),
(33, 600),
(35, 550),
(37, 650),
(39, 600);

-- Insert volunteer opportunities into the volunteer_opportunity table
INSERT INTO volunteer_opportunity (opportunity_id, max_participants, base_points, current_participants, start_time, end_time) VALUES
(2, 20, 100, 0, '09:00:00', '13:00:00'),
(4, 15, 100, 0, '14:00:00', '18:00:00'),
(6, 25, 100, 0, '10:00:00', '14:00:00'),
(8, 10, 100, 0, '08:00:00', '12:00:00'),
(10, 12, 100, 0, '15:00:00', '19:00:00'),
(12, 15, 100, 0, '10:00:00', '14:00:00'),
(14, 10, 100, 0, '13:00:00', '17:00:00'),
(16, 12, 100, 0, '09:00:00', '13:00:00'),
(18, 15, 100, 0, '14:00:00', '18:00:00'),
(20, 20, 100, 0, '10:00:00', '14:00:00'),
(22, 15, 100, 0, '08:00:00', '12:00:00'),
(24, 10, 100, 0, '14:00:00', '18:00:00'),
(26, 12, 100, 0, '15:00:00', '19:00:00'),
(28, 15, 100, 0, '09:00:00', '13:00:00'),
(30, 10, 100, 0, '14:00:00', '18:00:00'),
(32, 12, 100, 0, '10:00:00', '14:00:00'),
(34, 15, 100, 0, '09:00:00', '13:00:00'),
(36, 10, 100, 0, '14:00:00', '18:00:00'),
(38, 20, 100, 0, '10:00:00', '14:00:00'),
(40, 10, 100, 0, '09:00:00', '13:00:00');

-- Insert days for volunteer opportunities into the opportunity_day table
INSERT INTO opportunity_day (volunteer_opportunity_id, day_of_week) VALUES
(1, 'MONDAY'), (1, 'WEDNESDAY'),
(2, 'TUESDAY'), (2, 'THURSDAY'),
(3, 'SUNDAY'), (3, 'TUESDAY'),
(4, 'WEDNESDAY'), (4, 'FRIDAY'),
(5, 'MONDAY'), (5, 'THURSDAY'),
(6, 'TUESDAY'), (6, 'FRIDAY'),
(7, 'WEDNESDAY'), (7, 'SATURDAY'),
(8, 'MONDAY'), (8, 'THURSDAY'),
(9, 'TUESDAY'), (9, 'FRIDAY'),
(10, 'SUNDAY'), (10, 'WEDNESDAY'),
(11, 'MONDAY'), (11, 'THURSDAY'),
(12, 'TUESDAY'), (12, 'FRIDAY'),
(13, 'WEDNESDAY'), (13, 'SATURDAY'),
(14, 'MONDAY'), (14, 'WEDNESDAY'),
(15, 'TUESDAY'), (15, 'THURSDAY'),
(16, 'WEDNESDAY'), (16, 'FRIDAY'),
(17, 'MONDAY'), (17, 'THURSDAY'),
(18, 'TUESDAY'), (18, 'SATURDAY'),
(19, 'WEDNESDAY'), (19, 'FRIDAY'),
(20, 'MONDAY'), (20, 'THURSDAY');


-- Insert opportunity-skill associations into the opportunity_skills table using skill IDs
INSERT INTO opportunity_skills (opportunity_id, skill_id) VALUES
(1, 18), -- Emergency Response
(1, 32), -- Medical Training
(2, 8),  -- Community Engagement
(2, 40), -- Public Health
(3, 38), -- Project Management
(3, 17), -- Education
(4, 22), -- Event Planning
(4, 13), -- Cultural Preservation
(5, 14), -- Data Analysis
(5, 26), -- Healthcare Systems
(6, 30), -- Logistics
(6, 8),  -- Community Engagement
(7, 20), -- Environmental Science
(7, 42), -- Research
(8, 2),  -- Agriculture
(8, 8),  -- Community Engagement
(9, 1),  -- Advocacy
(9, 41), -- Public Speaking
(10, 23), -- Facilitation
(10, 39), -- Public Engagement
(11, 42), -- Research
(11, 29), -- Legal Analysis
(12, 35), -- Observation
(12, 16), -- Documentation
(13, 37), -- Program Management
(13, 47), -- Youth Engagement
(14, 31), -- Media Production
(14, 43), -- Social Media
(15, 25), -- Healthcare
(15, 10), -- Community Support
(16, 6),  -- Caregiving
(16, 8),  -- Community Engagement
(17, 45), -- Training
(17, 11), -- Conflict Resolution
(18, 23), -- Facilitation
(18, 47), -- Youth Engagement
(19, 38), -- Project Management
(19, 21), -- Environmental Sustainability
(20, 41), -- Public Speaking
(20, 19), -- Environmental Education
(21, 17), -- Education
(21, 25), -- Healthcare
(22, 25), -- Healthcare
(22, 10), -- Community Support
(23, 28), -- Legal Advocacy
(23, 48), -- Human Rights
(24, 10), -- Community Support
(24, 1),  -- Advocacy
(25, 36), -- Policy Analysis
(25, 42), -- Research
(26, 22), -- Event Planning
(26, 39), -- Public Engagement
(27, 45), -- Training
(27, 46), -- Youth Empowerment
(28, 24), -- Health Education
(28, 47), -- Youth Engagement
(29, 49), -- Mediation (new skill, ID 49)
(29, 11), -- Conflict Resolution
(30, 23), -- Facilitation
(30, 8),  -- Community Engagement
(31, 3),  -- Business Development
(31, 44), -- Strategic Planning
(32, 9),  -- Community Outreach
(32, 4),  -- Business Promotion
(33, 12), -- Counseling
(33, 33), -- Mental Health
(34, 41), -- Public Speaking
(34, 34), -- Mental Health Advocacy
(35, 7),  -- Community Development
(35, 38), -- Project Management
(36, 13), -- Cultural Preservation
(36, 8),  -- Community Engagement
(37, 5),  -- Campaign Management
(37, 1),  -- Advocacy
(38, 1),  -- Advocacy
(38, 9),  -- Community Outreach
(39, 42), -- Research
(39, 27), -- International Relations
(40, 42), -- Research
(40, 15); -- Data Collection


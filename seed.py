#!/usr/bin/env python3

from app import app  # Import your Flask app
from models import db, User, Post, Tag
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone
import random
import re

# Custom slugify function to avoid compatibility issues
def create_slug(text):
    """Create a URL-friendly slug from text"""
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def create_tables():
    """Create all database tables"""
    print("🏗️  Creating database tables...")
    db.create_all()
    print("✅ Tables created successfully!")

def clear_data():
    """Clear all existing data from the database"""
    print("🗑️  Clearing existing data...")
    
    try:
        # Clear association table first (if it exists)
        db.session.execute(db.text("DELETE FROM post_tags"))
        
        # Clear main tables
        Post.query.delete()
        Tag.query.delete()
        User.query.delete()
        
        db.session.commit()
        print("✅ Data cleared successfully!")
    except Exception as e:
        # If tables don't exist, that's fine - we'll create them
        print(f"⚠️  Tables may not exist yet (this is normal for first run): {str(e)}")
        db.session.rollback()

def create_users():
    """Create hospital staff users"""
    print("👥 Creating users...")
    
    users_data = [
        {
            'name': 'Dr. Alemnesh Bekele',
            'email': 'alemnesh.bekele@alerthospital.org',
            'password': 'password123',
            'bio': 'Chief Medical Director at Alert Hospital with over 15 years of experience in internal medicine. Passionate about improving healthcare access in rural Ethiopia.'
        },
        {
            'name': 'Dr. Solomon Tadesse',
            'email': 'solomon.tadesse@alerthospital.org',
            'password': 'password123',
            'bio': 'Senior Pediatrician specializing in childhood diseases and vaccination programs. Committed to reducing infant mortality in Ethiopia.'
        },
        {
            'name': 'Nurse Genet Assefa',
            'email': 'genet.assefa@alerthospital.org',
            'password': 'password123',
            'bio': 'Head Nurse with expertise in emergency care and patient education. Leading our community health outreach programs.'
        },
        {
            'name': 'Dr. Miriam Haile',
            'email': 'miriam.haile@alerthospital.org',
            'password': 'password123',
            'bio': 'OB/GYN specialist focused on maternal health and prenatal care. Director of our Women\'s Health Initiative.'
        },
        {
            'name': 'Admin Daniel Mekonnen',
            'email': 'daniel.mekonnen@alerthospital.org',
            'password': 'password123',
            'bio': 'Hospital Administrator with background in public health management. Oversees daily operations and community partnerships.'
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            password_hash=generate_password_hash(user_data['password']),
            bio=user_data['bio'],
            created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(30, 365))
        )
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    print(f"✅ Created {len(users)} users!")
    return users

def create_tags():
    """Create healthcare-related tags"""
    print("🏷️  Creating tags...")
    
    tag_names = [
        'Emergency Care', 'Pediatrics', 'Maternal Health', 'Surgery', 'Internal Medicine',
        'Vaccinations', 'Preventive Care', 'Nutrition', 'Mental Health', 'Diabetes',
        'Hypertension', 'HIV/AIDS', 'Malaria', 'Tuberculosis', 'Community Health',
        'Health Education', 'Medical Technology', 'Patient Stories', 'Hospital News',
        'Research', 'Wellness', 'First Aid', 'Chronic Diseases', 'Elderly Care',
        'Pharmacy', 'Laboratory', 'Radiology', 'Physical Therapy', 'Dental Care',
        'Oncology', 'Cardiology', 'Orthopedics', 'Neonatal Care', 'Public Health',
        'Health Policy', 'Medical Training', 'Telemedicine', 'Rural Health',
        'Traditional Medicine', 'Health Equity', 'Sanitation', 'Infectious Diseases'
    ]
    
    tags = []
    for tag_name in tag_names:
        tag = Tag(
            name=tag_name,
            slug=create_slug(tag_name)
        )
        tags.append(tag)
        db.session.add(tag)
    
    db.session.commit()
    print(f"✅ Created {len(tags)} tags!")
    return tags

def create_posts(users, tags):
    """Create hospital-related posts"""
    print("📝 Creating posts...")
    
    posts_data = [
        {
            'title': 'Alert Hospital Launches New Maternal Health Program',
            'excerpt': 'Our new initiative aims to reduce maternal mortality rates in the Addis Ababa region through improved prenatal care and education.',
            'body': '''# New Maternal Health Program at Alert Hospital

Alert Hospital is proud to announce the launch of our comprehensive Maternal Health Program, designed to support expectant mothers throughout their pregnancy journey.

## Program Overview

Our new initiative focuses on three key areas:

1. **Prenatal Care**: Regular check-ups, nutritional guidance, and risk assessment
2. **Delivery Services**: Modern facilities with skilled birth attendants
3. **Postnatal Support**: Follow-up care for mothers and newborns

## Services Offered

- Free prenatal vitamins for registered patients
- Educational workshops on childbirth and newborn care
- 24/7 emergency obstetric care
- Transportation assistance for high-risk pregnancies

## Our Goals

By implementing this program, we aim to:
- Reduce maternal mortality by 40% in our catchment area
- Increase prenatal care attendance by 60%
- Improve birth outcomes through early risk detection

## How to Participate

Expectant mothers can register at our maternity wing or through community health workers. The program is open to all residents of Addis Ababa and surrounding areas.

At Alert Hospital, we believe every mother deserves a safe pregnancy and delivery experience.''',
            'tags': ['Maternal Health', 'Hospital News', 'Community Health', 'Women\'s Health']
        },
        {
            'title': 'Understanding Malaria Prevention in Ethiopian Highlands',
            'excerpt': 'Learn about malaria risks and prevention strategies specific to the Ethiopian highlands region.',
            'body': '''# Malaria Prevention in the Ethiopian Highlands

While malaria is often associated with lowland areas, recent climate changes have increased risks in higher elevations. Here's what you need to know about prevention.

## Understanding the Risk

Malaria transmission in Ethiopia follows seasonal patterns, with peak transmission occurring from September to December after the rainy season. Our highland communities are becoming increasingly vulnerable.

## Prevention Strategies

### 1. Bed Nets
Insecticide-treated bed nets (ITNs) remain the most effective prevention method. Alert Hospital distributes free nets to vulnerable communities quarterly.

### 2. Environmental Management
- Eliminate standing water around homes
- Proper waste management to reduce mosquito breeding sites
- Community clean-up initiatives

### 3. Early Detection
Recognize symptoms early:
- Fever and chills
- Headache and body aches
- Fatigue
- Nausea and vomiting

## Alert Hospital's Initiatives

We operate:
- Free testing clinics in high-risk areas
- Educational programs in schools and community centers
- Partnership with local health extension workers

## When to Seek Help

If you experience malaria symptoms, visit our emergency department immediately. Early treatment prevents complications and reduces transmission.

Together, we can reduce malaria incidence in our communities.''',
            'tags': ['Malaria', 'Preventive Care', 'Infectious Diseases', 'Community Health']
        },
        {
            'title': 'Managing Diabetes: Lifestyle Changes for Better Health',
            'excerpt': 'Practical advice for diabetes management through diet, exercise, and regular monitoring.',
            'body': '''# Diabetes Management Strategies

Diabetes prevalence is rising in Ethiopia, but proper management can prevent complications and improve quality of life.

## Understanding Diabetes

Diabetes occurs when the body cannot properly process glucose, leading to high blood sugar levels. Type 2 diabetes, which is preventable, accounts for most cases in Ethiopia.

## Dietary Recommendations

### Traditional Foods for Diabetes Management

Many Ethiopian traditional foods can be part of a diabetes-friendly diet:

- **Injera**: Opt for teff injera, which has a lower glycemic index
- **Legumes**: Lentils, chickpeas, and beans provide sustained energy
- **Vegetables**: Include plenty of non-starchy vegetables like cabbage, carrots, and greens

### Foods to Limit

- Reduce portion sizes of carbohydrate-heavy foods
- Limit added sugars and sweetened beverages
- Moderate fruit consumption, focusing on lower-sugar options

## Physical Activity

Regular exercise helps control blood sugar levels. Aim for:

- 30 minutes of moderate activity most days
- Brisk walking, which is accessible to most people
- Traditional dancing as a fun form of exercise

## Alert Hospital's Diabetes Program

We offer:
- Free screening clinics on the first Tuesday of each month
- Nutrition counseling with culturally appropriate meal plans
- Support groups for patients and families
- Regular monitoring to prevent complications

## Medication Adherence

If prescribed medication:
- Take exactly as directed
- Never skip doses
- Report any side effects immediately

With proper management, people with diabetes can live full, active lives.''',
            'tags': ['Diabetes', 'Chronic Diseases', 'Nutrition', 'Preventive Care']
        },
        {
            'title': 'Emergency Preparedness: What Every Family Should Know',
            'excerpt': 'Essential first aid knowledge and emergency preparedness tips for Ethiopian households.',
            'body': '''# Emergency Preparedness for Families

Unexpected medical emergencies can happen anytime. Being prepared can make a critical difference in outcomes.

## Creating a Home First Aid Kit

Every household should have these basic supplies:

- Bandages, gauze, and adhesive tape
- Antiseptic solution and ointment
- Pain relievers (paracetamol/ibuprofen)
- Scissors, tweezers, and gloves
- Emergency contact numbers

## Common Emergency Situations

### Burns
- Cool the burn with running water for 10-15 minutes
- Cover with a clean, dry cloth
- Seek medical attention for severe burns

### Cuts and Wounds
- Apply direct pressure to stop bleeding
- Clean with clean water and soap
- Watch for signs of infection

### Fractures
- Immobilize the injured area
- Use makeshift splints if needed
- Seek immediate medical attention

## When to Come to the Emergency Department

Seek immediate care for:
- Difficulty breathing
- Chest pain
- Severe bleeding
- Loss of consciousness
- Poisoning
- Severe burns

## Alert Hospital Emergency Services

Our emergency department:
- Operates 24/7 with trained staff
- Has trauma specialists available
- Provides emergency surgery when needed
- Coordinates with ambulance services

## Preparing for Natural Disasters

Ethiopia faces various natural hazards. Prepare by:
- Knowing evacuation routes
- Having emergency water and food supplies
- Keeping important documents in a waterproof container

Being prepared saves lives. Learn basic first aid and keep emergency numbers handy.''',
            'tags': ['Emergency Care', 'First Aid', 'Health Education', 'Public Health']
        },
        {
            'title': 'The Importance of Vaccinations: Protecting Our Community',
            'excerpt': 'Understanding Ethiopia\'s vaccination schedule and how immunizations protect against preventable diseases.',
            'body': '''# Vaccination: Your Community's Health Shield

Vaccinations have dramatically reduced illness and death from infectious diseases worldwide. Here's what you need to know about immunization in Ethiopia.

## Ethiopia's Expanded Program on Immunization

The Ethiopian Ministry of Health provides free vaccinations for these preventable diseases:

- Tuberculosis
- Polio
- Diphtheria, Tetanus, and Pertussis (Whooping Cough)
- Hepatitis B
- Haemophilus influenzae type b
- Pneumococcal disease
- Rotavirus
- Measles
- Rubella

## Vaccination Schedule

### Childhood Immunizations
- **At birth**: BCG, OPV0
- **6 weeks**: Penta1, PCV1, Rota1, OPV1
- **10 weeks**: Penta2, PCV2, Rota2, OPV2
- **14 weeks**: Penta3, PCV3, OPV3
- **9 months**: Measles-Rubella 1

### Maternal Immunizations
- Tetanus Toxoid during pregnancy protects both mother and newborn

## Addressing Vaccine Concerns

### Are vaccines safe?
Yes. All vaccines undergo rigorous testing before approval and continuous monitoring after introduction.

### Can vaccines cause illness?
No. Vaccines contain weakened or inactivated viruses that cannot cause the actual disease.

### Why are so many doses needed?
Some vaccines require multiple doses to build strong immunity. Booster shots maintain protection over time.

## Alert Hospital Vaccination Services

We provide:
- Free vaccinations according to the national schedule
- Catch-up vaccinations for those who missed doses
- Education about vaccine benefits
- Cold chain maintenance to ensure vaccine potency

## Herd Immunity

When enough people are vaccinated, diseases can't spread easily, protecting those who can't be vaccinated (newborns, immunocompromised individuals).

Vaccination is one of the most effective public health interventions. Protect your family and community by staying up-to-date with immunizations.''',
            'tags': ['Vaccinations', 'Preventive Care', 'Pediatrics', 'Infectious Diseases']
        }
    ]

    # Add more hospital-related posts
    additional_posts = [
        {
            'title': 'Mental Health Support Services at Alert Hospital',
            'excerpt': 'Learn about our comprehensive mental health services and support programs for patients and families.',
            'body': 'Details about mental health services...',
            'tags': ['Mental Health', 'Wellness', 'Community Health']
        },
        {
            'title': 'Nutrition Workshop: Healthy Eating on a Budget',
            'excerpt': 'Join our free workshop on preparing nutritious meals using locally available ingredients.',
            'body': 'Information about nutrition workshop...',
            'tags': ['Nutrition', 'Health Education', 'Wellness']
        },
        {
            'title': 'Alert Hospital Expands Surgical Services',
            'excerpt': 'New operating theaters and specialized surgical team now available for complex procedures.',
            'body': 'Details about surgical expansion...',
            'tags': ['Surgery', 'Hospital News', 'Medical Technology']
        },
        {
            'title': 'Managing Hypertension: Silent Killer in Our Community',
            'excerpt': 'Understanding high blood pressure risks and management strategies for Ethiopian patients.',
            'body': 'Hypertension management information...',
            'tags': ['Hypertension', 'Chronic Diseases', 'Preventive Care']
        },
        {
            'title': 'Community Health Workers: Bridging Healthcare Gaps',
            'excerpt': 'How our network of health extension workers brings healthcare to remote communities.',
            'body': 'Information about community health workers...',
            'tags': ['Community Health', 'Public Health', 'Rural Health']
        }
    ]

    posts_data.extend(additional_posts)
    
    posts = []
    for i, post_data in enumerate(posts_data):
        # Random author
        author = random.choice(users)
        
        # Random creation date (within last 6 months)
        created_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 180))
        
        # Random status (mostly published)
        status = random.choices(['published', 'draft', 'archived'], weights=[0.8, 0.15, 0.05])[0]
        
        # Set published date if status is published
        published_at = created_date + timedelta(hours=random.randint(1, 48)) if status == 'published' else None
        
        post = Post(
            title=post_data['title'],
            slug=create_slug(post_data['title']),
            excerpt=post_data['excerpt'],
            body=post_data['body'],
            status=status,
            author_id=author.id,
            created_at=created_date,
            published_at=published_at,
            views=random.randint(10, 1000) if status == 'published' else 0
        )
        
        # Add random tags
        available_tags = [tag for tag in tags if tag.name in post_data['tags']]
        post_tags = random.sample(available_tags, min(len(available_tags), random.randint(2, 5)))
        post.tags.extend(post_tags)
        
        posts.append(post)
        db.session.add(post)
    
    db.session.commit()
    print(f"✅ Created {len(posts)} posts!")
    return posts

def seed_database():
    """Main seeding function"""
    print("🌱 Starting database seeding...")
    
    with app.app_context():
        # Create tables if they don't exist
        create_tables()
        
        # Clear existing data
        clear_data()
        
        # Create sample data
        users = create_users()
        tags = create_tags()
        posts = create_posts(users, tags)
        
        print("🎉 Database seeding completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Users: {len(users)}")
        print(f"   - Tags: {len(tags)}")
        print(f"   - Posts: {len(posts)}")

if __name__ == '__main__':
    seed_database()
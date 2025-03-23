# SELL UR STUFF - APP / SITE



## Table of Contents

- [SELL UR STUFF - APP / SITE](#sell-ur-stuff---app--site)
  - [Table of Contents](#table-of-contents)
  - [Project Purpose](#project-purpose)
  - [Target Audience](#target-audience)
  - [The Problem It Solves](#the-problem-it-solves)
  - [User Stories](#user-stories)
    - [A. Seller Stories](#a-seller-stories)
    - [B. Buyer Stories](#b-buyer-stories)
    - [C. Administrator Stories](#c-administrator-stories)
  - [Project Requirements](#project-requirements)
    - [A. E-commerce Requirements](#a-e-commerce-requirements)
    - [B. Authentication \& Authorization Requirements](#b-authentication--authorization-requirements)
  - [Tech Stack](#tech-stack)
  - [Agile Workflow](#agile-workflow)
    - [GitHub Issues](#github-issues)
    - [GitHub Project Board](#github-project-board)
    - [Sprints](#sprints)
  - [Setup Instructions](#setup-instructions)
    - [Prerequisites](#prerequisites)
    - [Local Development Setup](#local-development-setup)
    - [Media Storage (Local)](#media-storage-local)
  - [Deployment to Heroku](#deployment-to-heroku)
    - [Prerequisites](#prerequisites-1)
    - [Deployment Steps](#deployment-steps)
    - [Media Storage (Production)](#media-storage-production)
  - [Known Issues](#known-issues)
  - [Future Enhancements](#future-enhancements)
  - [Contact](#contact)

---

## Project Purpose

The purpose of this application is to revolutionize the online classifieds marketplace by building a user-friendly, dynamic platform that facilitates buying and selling items while leveraging multimedia. Unlike traditional classifieds sites, our application integrates video functionality, allowing sellers to upload short videos showcasing their products. This visual component provides buyers with a more comprehensive and engaging view of items, increasing trust and speeding up the sales process.

Sellers can also boost their product visibility by paying for a 24-hour feature on a dedicated “Sales Blitz” page. This premium service ensures prominent placement and increased exposure to potential buyers, helping sellers secure quicker sales.

## Target Audience

- **Private Sellers**: Individuals looking to offload personal belongings quickly, from household items to gadgets, without complex listing procedures.
- **Casual Sellers**: Users with small inventories who want an intuitive, visually appealing platform to test online selling.
- **Tech-Savvy Users**: Individuals comfortable with multimedia-rich platforms, seeking a modern alternative to traditional classifieds.
- **Value Seekers**: Buyers who value transparency through video listings for informed purchase decisions.

## The Problem It Solves

Traditional classified platforms often have outdated interfaces, lack multimedia integration, and offer limited visibility options for sellers, leading to slower sales and a less engaging experience. Our application addresses these issues by:

- **Enhancing User Experience**: Providing a modern, streamlined interface that’s accessible and intuitive.
- **Multimedia Integration**: Allowing video uploads for richer, more engaging content that builds buyer confidence.
- **Paid Boost Options**: Offering a 24-hour “Sales Blitz” page for increased exposure and faster sales.
- **Targeted Functionality**: Catering to private and casual sellers while appealing to tech-savvy consumers.

## User Stories

### A. Seller Stories

- **Seller-01**: As a seller, I want to register an account to list and manage my products securely.
- **Seller-02**: As a seller, I want to create a product listing with descriptions and a video to give buyers a clear, engaging view.
  - *Example*: The "Create Listing" form allows sellers to add a title, description, price, and upload images/videos.
  
    ![Create Listing Form](/sell_ur_stuff/static/images/readme/sale_create.png)  
    *Caption*: The "Create Listing" form where sellers can input details and upload media for their products.

- **Seller-03**: As a seller, I want to edit or delete listings to manage outdated or sold items.

  - *Example*: The "Your Offers" section shows the status of offers and provides a "Pay Now" option for accepted offers.
  
    ![Your Offers Section](/sell_ur_stuff/static/images/readme/offer_page.png)  
    *Caption*: The "Your Offers" section displaying an accepted offer with a "Pay Now" button.

### B. Buyer Stories

- **Buyer-01**: As a buyer, I want to browse and search for product listings to find items that interest me.
  - *Example*: Listings are categorized into "Active," "Sold," and "Pending" tabs for easy browsing.
  
    ![Listing Tabs](/sell_ur_stuff/static/images/readme/listing_table.png)  
    *Caption*: Tabs for browsing listings: "Active," "Sold," and "Pending."

- **Buyer-02**: As a buyer, I want to view detailed product pages with text and video for informed decisions.
  - *Example*: A product listing for "headphones" shows the price, status, and a preview image.
  
    ![Product Listing](/sell_ur_stuff/static/images/readme/item_sections.png)  
    *Caption*: A product listing for "headphones" with price and status details.

- **Buyer-03**: As a buyer, I want to contact sellers securely via a messaging system without leaving the platform.
- **Buyer-04**: As a buyer, I want clear feedback when interacting with the site to know what to expect.
  - *Example*: After making an offer, buyers receive feedback if the offer is too low or accepted.
  
    ![Offer Feedback](/sell_ur_stuff/static/images/readme/buyer_offer_payment.png)  
    *Caption*: Feedback message indicating an offer is below the minimum threshold.

### C. Administrator Stories

- **Admin-01**: As an administrator, I want to manage user accounts and roles to ensure authorized access.
- **Admin-02**: As an administrator, I want to review and moderate listings and content to maintain quality.
- **Admin-03**: As an administrator, I want to view reports on sales, user activity, and boost transactions to assess performance.
- **Admin-04**: As an administrator, I want to manage payment transactions for smooth e-commerce functionality.
- **Admin-05**: As an administrator, I want to configure SEO settings and monitor site indexing for optimal visibility.

## Project Requirements

### A. E-commerce Requirements

- Integrate an online payment system (e.g., Stripe) for boosted listings.
  - *Example*: A confirmation message appears after a successful payment.
  
    ![Payment Successful](/sell_ur_stuff/static/images/readme/payment_processed.png)  
    *Caption*: Payment confirmation message after purchasing "headphones."

- Enable video uploads with validations (file type, size, etc.).
- Create an administrative dashboard for reviewing transactions and sales performance.

### B. Authentication & Authorization Requirements

- Implement secure registration and login pages using Django’s authentication framework.
- Define roles and restrict access based on user permissions.
- Ensure security best practices for sensitive data handling.

## Tech Stack

- **Framework**: Django 5.1.6
- **Language**: Python 3.13.1
- **Database**:
  - Local: SQLite
  - Production: PostgreSQL (via Heroku)
- **Media Storage**:
  - Local: Filesystem (`MEDIA_ROOT`)
  - Production: Amazon S3 (using `django-storages` and `boto3`)
- **Static Files**: Whitenoise (for serving static files on Heroku)
- **Authentication**: Django Allauth
- **Payment Processing**: Stripe
- **Deployment**: Heroku
- **Environment Management**: `python-dotenv` for managing environment variables

## Agile Workflow

This project uses GitHub Issues and Projects to manage development in an Agile manner, with sprints and a Kanban board to track progress.

[Sell Your Stuff ERD](https://dbdocs.io/terryloughran/Sell-Your-Stuff) for further project flow.

### GitHub Issues

- Each user story and task is documented as a GitHub Issue.
- Issues are labeled (e.g., `user-story`, `seller`, `buyer`, `admin`, `task`) and assigned to milestones (sprints).
- Example: [User Story] Seller-01: Register an Account (#2)

### GitHub Project Board

- The project board is divided into columns: **Backlog**, **To Do**, **In Progress**, **In Review**, and **Done**.
- Issues are moved through these columns as work progresses.
- Link to the project board: [Sell Ur Stuff Project Board](https://github.com/users/TerryLoc/projects/4).

### Sprints

- **Sprint 1 (Setup and Authentication)**:
  - Issues: `Project Setup and Environment Configuration (#1)`, `Authentication & Authorization (#2)`
  - Focus: Set up the project environment and implement user registration/login.
- **Sprint 2 (Product Listings and E-commerce)**:
  - Issues: `Product Listing and CRUD Operations (#3)`, `E-commerce and Payment Integration (#4)`
  - Focus: Implement product listings with video uploads and Stripe payment for boosts.
- **Sprint 3 (UX and SEO)**:
  - Issues: `Front-End Design and User Experience (UX) (#5)`, `SEO and Marketing Integration (#6)`
  - Focus: Enhance the UI/UX and implement SEO features.

## Setup Instructions

### Prerequisites

- Python 3.13.1 or higher
- Git
- Heroku CLI (for deployment)
- An AWS account (for S3 storage in production)
- A Stripe account (for payment processing)

### Local Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/sell-ur-stuff.git
   cd sell-ur-stuff
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root (`sell_ur_stuff/.env`):
     ```env
     DEBUG=True
     SECRET_KEY=your-secret-key
     STRIPE_PUBLIC_KEY=your-stripe-public-key
     STRIPE_SECRET_KEY=your-stripe-secret-key
     ```
   - Generate a `SECRET_KEY` (e.g., using Django’s `get_random_secret_key()` in a Python shell).

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (Admin)**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

8. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   - Access the site at `http://localhost:8000/`.
   - Access the admin panel at `http://localhost:8000/admin/`.

### Media Storage (Local)

- Media files (e.g., profile pictures, videos) are stored locally in `sell_ur_stuff/media/`.
- Ensure the `media` directory exists:
  ```bash
  mkdir -p media/profile_pics
  ```

## Deployment to Heroku

### Prerequisites

- A Heroku account and the Heroku CLI installed.
- An Amazon S3 bucket for media storage.
- A PostgreSQL database (Heroku Postgres add-on).

### Deployment Steps

1. **Log in to Heroku**:
   ```bash
   heroku login
   ```

2. **Create a Heroku App** (if not already created):
   ```bash
   heroku create sell-ur-stuff-19632c616966
   ```

3. **Add Heroku Postgres**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set Environment Variables**:
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set STRIPE_PUBLIC_KEY=your-stripe-public-key
   heroku config:set STRIPE_SECRET_KEY=your-stripe-secret-key
   heroku config:set AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
   heroku config:set AWS_S3_REGION_NAME=your-s3-region
   heroku config:set AWS_ACCESS_KEY_ID=your-aws-access-key
   heroku config:set AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   ```

5. **Deploy the App**:
   ```bash
   git add .
   git commit -m "Prepare for Heroku deployment"
   git push heroku main
   ```

6. **Run Migrations on Heroku**:
   ```bash
   heroku run python manage.py migrate
   ```

7. **Create a Superuser on Heroku**:
   ```bash
   heroku run python manage.py createsuperuser
   ```

8. **Collect Static Files**:
   - Whitenoise will handle static files automatically on Heroku.

9. **Access the Live Site**:
   - Open the app:
     ```bash
     heroku open
     ```
   - The site should be live at `https://sell-ur-stuff-19632c616966.herokuapp.com/`.

### Media Storage (Production)

- Media files are stored in an Amazon S3 bucket.
- Ensure your S3 bucket has a public read policy for objects:
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::bucket-name/*"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam:::account-id/the-user"
            },
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": "arn:aws:s3:::bucket-name/*"
        }
    ]

- Adjust the S3 bucket’s Block Public Access settings to allow public read access via policies:
  - Uncheck “Block all public access”.
  - Keep ACL blocking enabled for security.
  - Uncheck policy blocking to allow public read access via the bucket policy.

## UX Design

### Design Process

The UX design for **Sell Ur Stuff** focused on creating an intuitive and engaging experience for private sellers, casual sellers, tech-savvy users, and value seekers. The process included:

### Wireframes

- Created wireframes for key pages (e.g., homepage, product listing page, profile page) using tools like Figma.
- **Homepage**: Featured a search bar, featured listings (Sales Blitz), and navigation links to Market, Profiles, and Contact.
- **Product Listing Page**: Included a video player, product description, and a “Contact Seller” button.
- **Profile Page**: Displayed the user’s profile picture, a list of their listings, and an “Edit Profile” button.

### Mockups

- Developed high-fidelity mockups to finalize the design.
- Used a clean, modern design with a focus on multimedia (e.g., large video player for product listings).
- Ensured responsiveness with a mobile-first approach (e.g., collapsible navigation menu on mobile).

### User Feedback

- Conducted informal user testing with peers to gather feedback on usability.
- Adjusted the design to improve navigation (e.g., added a “Back to Listings” button on product pages).

### Implementation

The wireframes and mockups were implemented using Django templates and Bootstrap for styling.

- **Homepage**: `templates/home/home.html` includes a search bar and featured listings.
- **Product Listing Page**: `templates/market/listing_detail.html` includes a video player.
- **Profile Page**: `templates/profiles/profile.html` displays the user’s profile picture (`<img src="">`) and listings.
- The design ensures responsiveness across devices, tested using Chrome DevTools.

### Diagrams

- Wireframes and mockups are stored in the `docs/ux/` directory (create this directory if it doesn’t exist).
- Example: `docs/ux/homepage-wireframe.png`, `docs/ux/product-listing-mockup.png`.

## Testing

Testing procedures are documented in [TESTING.md](TESTING.md). Key areas include:

- **Functionality**: Tested all user stories (e.g., registration, product listing creation, payment for boosts).
- **Usability**: Ensured intuitive navigation and clear feedback (e.g., form validation errors).
- **Responsiveness**: Tested on multiple devices using Chrome DevTools.
- **Data Management**: Verified media storage (local filesystem and S3) and database operations.
- Automated tests are implemented in each app (e.g., `profiles/tests.py` for profile picture uploads).

## Project Structure

```
sell_ur_stuff/
├── home/                # App for homepage functionality
├── sales/               # App for Sales Blitz and boost features
├── market/              # App for product listings and browsing
├── profiles/            # App for user profiles and media uploads
├── contact/             # App for contact/inquiry system
├── static/              # Static files (CSS, JS, images)
├── media/               # Media files (local development only)
├── templates/           # Base templates and shared HTML
├── sell_ur_stuff_site/  # Project settings and URLs
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (not tracked in git)
```

## Issues Encountered

During development, we faced several challenges, which are documented here for reference:

- **Media Serving in Development**:
  - **Issue**: Profile pictures (e.g., `glass-3077869_640.jpg`) were not displaying locally, returning a 404 error at `http://localhost:8000/media/profile_pics/glass-3077869_640.jpg`, despite the file existing in `sell_ur_stuff/media/profile_pics/`.
  - **Cause**: The `DEBUG` setting was evaluating to `False` due to an incorrect comparison (`os.getenv("DEBUG", False) == True`), preventing Django from serving media files via `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` in `urls.py`.
  - **Resolution**: Updated the `DEBUG` setting to compare strings (`os.getenv("DEBUG", "False") == "True"`), ensuring `DEBUG` was `True` in development. Added debugging print statements to confirm the `.env` file was loaded correctly.

- **S3 Configuration in Production**:
  - **Issue**: Images were not accessible on Heroku after switching from Cloudinary to Amazon S3, due to S3’s Block Public Access settings.
  - **Cause**: The S3 bucket had “Block all public access” enabled, preventing public read access to objects, even with a bucket policy allowing `s3:GetObject`.
  - **Resolution**: Adjusted the Block Public Access settings to allow public read access via bucket policies (unchecked “Block public access to buckets and objects granted through new public bucket or access point policies” and “Block public and cross-account access...”). Added a bucket policy to allow public read access to objects.

- **Cloudinary Leftovers**:
  - **Issue**: `cloudinary` and `cloudinary_storage` were still in `INSTALLED_APPS`, causing potential conflicts after switching to S3.
  - **Resolution**: Removed `cloudinary` and `cloudinary_storage` from `INSTALLED_APPS` and uninstalled them from `requirements.txt`.

- **Database Configuration Missing**:
  - **Issue**: The `DATABASES` setting was missing in `settings.py`, which could cause issues on Heroku.
  - **Resolution**: Added `dj_database_url` to parse `DATABASE_URL` on Heroku and configured `DATABASES` to use SQLite locally and PostgreSQL in production.

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a pull request on GitHub.

## Known Issues

- **Email Verification**: Currently set to `none` (`ACCOUNT_EMAIL_VERIFICATION = "none"`). Set to `mandatory` in production and configure an email backend (e.g., SendGrid).
- **Video Uploads**: Ensure video file validations (size, format) are implemented in the `market` app.
- **Images**: I cannot seem to get the images to show on the live site. I tried `cloudinary` and am now using `AWS`, but I cannot get either to allow me to upload. I have hit a wall!

## Future Enhancements

- Add a messaging system for secure buyer-seller communication.
- Implement video compression for faster uploads and streaming.
- Add analytics for sellers to track listing views and engagement.
- Integrate a review/rating system for buyers and sellers.
- Enhance the newsletter subscription feature with better user feedback.

## Contact

For questions or support, contact the project maintainer [TERRY](https://github.com/TerryLoc).
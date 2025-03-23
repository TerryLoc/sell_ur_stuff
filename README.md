
---

# SELL UR STUFF - APP / SITE

## Project Purpose

The purpose of this application is to revolutionize the online classifieds marketplace by building a user-friendly, dynamic platform that not only facilitates the buying and selling of items but also leverages the power of multimedia. Unlike traditional classifieds sites, our application integrates video functionality, allowing sellers to upload short videos showcasing their products. This visual component aims to give buyers a more comprehensive and engaging view of the items on offer, thereby increasing trust and speeding up the sales process.

In addition to the enhanced listing experience, sellers have the option to boost their product visibility by paying for a 24-hour feature on a dedicated “Sales Blitz” page. This premium service is designed to help sellers secure quicker sales by giving their listings prominent placement and increased exposure to potential buyers actively searching for deals.

## Target Audience

- **Private Sellers**: Individuals looking to offload personal belongings quickly, from household items to personal gadgets, without the hassle of complex listing procedures.
- **Casual Sellers**: Users who may not have a large inventory but want to test the waters of online selling using an intuitive and visually appealing platform.
- **Tech-Savvy Users**: Individuals who are comfortable with using modern, multimedia-rich platforms and are looking for a more engaging alternative to traditional classifieds.
- **Value Seekers**: Buyers who appreciate the transparency provided by video listings, enabling them to make more informed purchase decisions.

## The Problem It Solves

Traditional classified advertisement platforms often suffer from outdated user interfaces, a lack of multimedia integration, and limited options for sellers to enhance the visibility of their listings. These challenges result in slower sales cycles and a less engaging experience for both buyers and sellers.

Our application addresses these issues by:

- **Enhancing User Experience**: Offering a modern, streamlined interface that is both accessible and intuitive, encouraging users to interact more deeply with listings.
- **Multimedia Integration**: Allowing sellers to upload videos, thereby providing richer, more engaging content that builds buyer confidence and increases conversion rates.
- **Paid Boost Options**: Giving sellers the ability to pay for increased exposure via a dedicated 24-hour sales page, which promotes rapid turnover and caters to users in need of a quick sale.
- **Targeted Functionality**: Focusing on private and casual sellers who seek a more efficient marketplace solution, while also offering the technological edge that appeals to the modern, tech-savvy consumer.

## User Stories

### A. Seller Stories

- **Seller-01**: As a seller, I want to register an account so that I can list my products securely and manage my listings over time.
- **Seller-02**: As a seller, I want to create a product listing with detailed descriptions and upload a video showcasing my product so that buyers get a clear and engaging view of the item.
- **Seller-03**: As a seller, I want to edit or delete my listings so that I can manage outdated or sold items easily.
- **Seller-04**: As a seller, I want to pay for a 24-hour boost to feature my listing on a dedicated “Sales Blitz” page so that my product gets increased exposure for a quicker sale.
- **Seller-05**: As a seller, I want to view the status of my listings and any boost transactions so that I can track the effectiveness of my promotional efforts.

### B. Buyer Stories

- **Buyer-01**: As a buyer, I want to browse and search for product listings so that I can easily find items that interest me.
- **Buyer-02**: As a buyer, I want to view detailed product pages that include both text and video so that I can make informed purchasing decisions.
- **Buyer-03**: As a buyer, I want to contact sellers securely through a messaging or inquiry system so that I can ask questions about a product without leaving the platform.
- **Buyer-04**: As a buyer, I want clear feedback when interacting with the site so that I always know what to expect next.

### C. Administrator Stories

- **Admin-01**: As an administrator, I want to manage user accounts and roles so that I can ensure only authorized users have access to sensitive operations.
- **Admin-02**: As an administrator, I want to review and moderate product listings and user-generated content to maintain quality and compliance with site policies.
- **Admin-03**: As an administrator, I want to view reports on sales, user activity, and boost transactions so that I can assess the platform’s performance and address issues proactively.
- **Admin-04**: As an administrator, I want to manage payment transactions so that the e-commerce functionality operates smoothly.
- **Admin-05**: As an administrator, I want to configure SEO settings and monitor site indexing so that the platform achieves optimal online visibility.

## Project Requirements

### A. E-commerce Requirements

- Integrate an online payment system (e.g., Stripe) to handle transactions for boosted listings.
- Enable video uploads with validations (file type, size, etc.).
- Create an administrative dashboard for reviewing transactions and overall sales performance.

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
              "Resource": "arn:aws:s3:::your-bucket-name/*"
          }
      ]
  }
  ```
- Adjust the S3 bucket’s Block Public Access settings to allow public read access via policies:
  - Uncheck “Block all public access”.
  - Keep ACL blocking enabled for security.
  - Uncheck policy blocking to allow public read access via the bucket policy.

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

During development, we ran into several challenges that were resolved. These are documented here for future reference:

- **Media Serving in Development**:
  - **Issue**: Profile pictures (e.g., `glass-3077869_640.jpg`) were not displaying locally, returning a 404 error at `http://localhost:8000/media/profile_pics/glass-3077869_640.jpg`, despite the file existing in `sell_ur_stuff/media/profile_pics/`.
  - **Cause**: The `DEBUG` setting was evaluating to `False` due to an incorrect comparison (`os.getenv("DEBUG", False) == True`), preventing Django from serving media files via `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` in `urls.py`.
  - **Resolution**: Updated the `DEBUG` setting to compare strings (`os.getenv("DEBUG", "False") == "True"`), ensuring `DEBUG` was `True` in development. Added debugging print statements to confirm the `.env` file was loaded correctly.

- **S3 Configuration in Production**:
  - **Issue**: Images were not accessible on Heroku after switching from Cloudinary to Amazon S3, due to S3’s Block Public Access settings.
  - **Cause**: The S3 bucket had “Block all public access” enabled, which prevented public read access to objects, even with a bucket policy allowing `s3:GetObject`.
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

## Future Enhancements

- Add a messaging system for secure buyer-seller communication.
- Implement video compression for faster uploads and streaming.
- Add analytics for sellers to track listing views and engagement.
- Integrate a review/rating system for buyers and sellers.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, contact the project maintainer at [your-email@example.com].

---

### Notes for You
- **GitHub Repository**: Replace `https://github.com/your-username/sell-ur-stuff.git` with the actual repository URL.
- **Email**: Update the contact email in the “Contact” section.
- **License**: Add a `LICENSE` file to your repository if you haven’t already (e.g., MIT License).
- **Issues Encountered**: I’ve included the main issues we faced (media serving, S3 configuration, Cloudinary leftovers, and database setup). Let me know if you’d like to add more.
- **Future Enhancements**: Modify this section based on your roadmap if needed.

This README provides a detailed overview of the project, setup instructions, deployment steps, and a record of the issues we encountered, making it a valuable resource for anyone working on **Sell Your Stuff**. Let me know if you’d like to adjust any sections! 💚 Sláinte! 🚀
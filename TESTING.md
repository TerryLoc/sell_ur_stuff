
# Testing Procedures for Sell Ur Stuff

This document outlines the testing procedures for the **Sell Ur Stuff** application, covering functionality, usability, responsiveness, and data management. It also includes details about automated tests implemented in `profiles/tests.py`.

## Automated Testing

Automated tests are implemented using Django’s testing framework to ensure the reliability of key features in the `profiles` app. Below is the content of `profiles/tests.py`, which tests the `UserProfile` model.


```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile
import os.path

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)

    def test_profile_picture_upload(self):
        # Create a dummy image file for testing
        image = SimpleUploadedFile(
            name="test.jpg",
            content=b"file_content",  # Dummy content (simulates file data)
            content_type="image/jpeg",
        )
        self.profile.profile_picture = image
        self.profile.save()
        # Extract the base filename and check if it starts with "test" and ends with ".jpg"
        base_name = os.path.basename(self.profile.profile_picture.name)
        self.assertTrue(base_name.startswith("test") and base_name.endswith(".jpg"))

    def test_profile_string_representation(self):
        self.assertEqual(str(self.profile), f"{self.user.username}'s profile")
```

#### Test Cases Explained

| Test Method                          | Description                                                       | Assertion                                                                                               |
| ------------------------------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `test_profile_picture_upload`        | Tests the upload of a profile picture to the `UserProfile` model. | Verifies that the uploaded file’s name starts with "test" and ends with ".jpg".                         |
| `test_profile_string_representation` | Tests the string representation of the `UserProfile` model.       | Ensures the string representation is in the format `<username>'s profile` (e.g., "testuser's profile"). |

#### Running the Tests
To run the automated tests, use the following command:
```bash
python manage.py test profiles
```

## Manual Testing Procedures

### 1. Functionality Testing

**Objective**: Ensure all user stories are implemented correctly.

| User Story                                       | Procedure                                                                                                                                                                                                                          |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Seller-01: Register an Account**               | - Navigate to the registration page (`/accounts/signup/`).<br>- Enter a username, email, and password.<br>- Verify a confirmation message is displayed.<br>- Log in with the new credentials.                                      |
| **Seller-02: Create Product Listing with Video** | - Log in as a seller.<br>- Go to the listing creation page (`/market/create/`).<br>- Fill in the form with a description and upload a video (e.g., MP4 file < 10MB).<br>- Verify the listing is created and the video is playable. |
| **Seller-03: Edit or Delete Listings**           | - Log in as a seller.<br>- Go to the profile page (`/profiles/`).<br>- Edit a listing and verify changes are saved.<br>- Delete a listing and verify it’s removed from the marketplace.                                            |
| **Seller-04: Pay for a 24-Hour Boost**           | - Log in as a seller.<br>- Go to a listing and click “Boost”.<br>- Complete the Stripe payment.<br>- Verify the listing appears on the “Sales Blitz” page for 24 hours.                                                            |
| **Seller-05: View Listing and Boost Status**     | - Log in as a seller.<br>- Go to the profile page.<br>- Verify the table shows listing status and boost status (e.g., time remaining).                                                                                             |
| **Buyer-01: Browse**                             | - Go to the marketplace page (`/market/`).<br>- Browse listings and verify pagination.                                                                                                                                             |
| **Buyer-02: View Detailed Product Pages**        | - Click on a listing from the marketplace.<br>- Verify the detail page shows title, description, price, and a playable video.                                                                                                      |
| **Buyer-03: Buying process**                     | Buyer can offer and pay for items that wish to purchase                                                                                                                                                                            |
| **Admin-01: Manage User Accounts and Roles**     | - Log in as an admin.<br>- Go to the admin panel (`/admin/`).<br>- Edit a user’s role (e.g., make them staff).<br>- Verify non-admin users cannot access the admin panel.                                                          |


### 2. Usability Testing

**Objective**: Ensure the interface is intuitive and user-friendly.

| Test Case          | Procedure                                                                                                                  |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **Navigation**     | Ensure all links (e.g., Home, Market, Profiles) work and are clearly labeled.                                              |
| **Forms**          | Verify that forms (e.g., registration, listing creation) provide clear feedback (e.g., error messages for invalid inputs). |
| **Video Playback** | Ensure videos play smoothly on desktop and mobile devices.                                                                 |

### 3. Responsiveness Testing

**Objective**: Ensure the site is responsive across devices.

| Test Case                | Procedure                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------- |
| **Device Compatibility** | Use Chrome DevTools to test on different screen sizes (e.g., iPhone 14, iPad, Desktop).           |
| **Layout Adjustment**    | Verify that the layout adjusts correctly (e.g., profile picture and video player are responsive). |
| **Mobile Navigation**    | Test navigation menu on mobile: Ensure it collapses into a hamburger menu.                        |

### 4. Data Management Testing

**Objective**: Ensure data is stored and retrieved correctly.

| Environment         | Procedure                                                                                                                                                                                                                                       |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Local (SQLite)**  | - Create a listing with a video and verify it’s saved in `media/`.<br>- Delete the listing and verify the file is removed.                                                                                                                      |
| **Production (S3)** | - Upload a profile picture on Heroku and verify it’s stored in the S3 bucket.<br>- Check the S3 bucket to ensure the file exists (e.g., `profile_pics/glass-3077869_640.jpg`).<br>- Delete the profile picture and verify it’s removed from S3. |

---

### Testing Payment

The **Sell Ur Stuff** application uses Stripe for payment processing. To ensure payment functionality works correctly without risking real transactions, testing is conducted in a sandbox environment using Stripe's test mode.

#### Use a Sandbox Environment

- Set up Stripe in test mode by using your Stripe test API keys in the `.env` file:
  ```env
  STRIPE_PUBLIC_KEY=pk_test_your-test-public-key
  STRIPE_SECRET_KEY=sk_test_your-test-secret-key
  ```
- Use Stripe's provided test cards to simulate transactions. These cards work with any future expiration date (e.g., `12/25`) and a CVV (e.g., `123` for Visa/MasterCard, `1234` for Amex). Common test card numbers include:

  | Card Type            | Test Card Number      | Notes                                |
  | -------------------- | --------------------- | ------------------------------------ |
  | **Visa**             | `4111 1111 1111 1111` | General-purpose test card.           |
  | **MasterCard**       | `5555 5555 5555 4444` | General-purpose test card.           |
  | **American Express** | `3782 822463 10005`   | Requires 4-digit CVV (e.g., `1234`). |

#### Test Scenarios

Test the payment functionality for boosting a listing using the following scenarios:

| Scenario                   | Test Card Number      | Expected Outcome                         | Steps to Test                                                                                                                                                                                                                           |
| -------------------------- | --------------------- | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Successful Transaction** | `4242 4242 4242 4242` | Payment succeeds, listing is boosted.    | - Log in as a seller.<br>- Go to a listing and click "Boost".<br>- Enter the card details (e.g., `4242 4242 4242 4242`, expiry `12/25`, CVV `123`).<br>- Verify the payment succeeds and the listing appears on the "Sales Blitz" page. |
| **Declined Transaction**   | `4000 0000 0000 9995` | Payment fails with "insufficient funds". | - Repeat the steps above with the card `4000 0000 0000 9995`.<br>- Verify an error message is displayed indicating the payment was declined.                                                                                            |
| **3D Secure**              | `4000 0000 0000 3220` | Payment portal appeared                  | Stripe 3D Secure test card. Testing work and confirmation of purchase page was generated.                                                                                                                                               | - Note: 3D Secure testing requires a specific test card (e.g., `4000 0000 0000 3220` for Stripe). This scenario is not currently implemented but can be added in the future. |

#### Notes
- Ensure Stripe is configured in test mode during development and testing to avoid real charges.
- After testing, verify that the admin dashboard (`/admin/`) correctly reflects the test transactions (e.g., for Admin-04: Manage Payment Transactions).

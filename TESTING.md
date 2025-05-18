
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

---

## Fixing Storage Backend Issue: Ensuring `CustomS3Boto3Storage` Is Used

### Overview
The goal was to ensure that Django uses `CustomS3Boto3Storage` (configured to upload files to an S3 bucket) instead of the default `FileSystemStorage`. Initially, despite setting `DEFAULT_FILE_STORAGE` to `sell_ur_stuff_site.storage.CustomS3Boto3Storage`, `default_storage` remained `FileSystemStorage`, causing images not to upload to S3 and not appear on the `/market/` page unless manually uploaded. Below is a breakdown of the debugging and resolution process.

### Problem Identification
| **Step**                  | **Action**                                                          | **Observation**                                                             | **Conclusion**                                                                                        |
| ------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Check `default_storage`   | Ran `print(f"Storage class: {default_storage.__class__.__name__}")` | Output: `Storage class: FileSystemStorage`                                  | `default_storage` is not using `CustomS3Boto3Storage` despite `DEFAULT_FILE_STORAGE` being set.       |
| Verify `settings.py`      | Checked `DEFAULT_FILE_STORAGE` setting                              | `DEFAULT_FILE_STORAGE = "sell_ur_stuff_site.storage.CustomS3Boto3Storage"`  | Setting is correct, but Django isn’t applying it.                                                     |
| Test manual instantiation | Instantiated `CustomS3Boto3Storage` manually in shell               | Successfully instantiated, bucket name: `sellyourtuff`, region: `eu-west-1` | `CustomS3Boto3Storage` class works when manually instantiated, issue is with Django’s initialization. |

### Debugging Steps
| **Step**                              | **Action**                                                             | **Code/Change**                                                                                 | **Result**                                                                                   |
| ------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Add debug prints to `settings.py`     | Added prints to trace `settings.py` loading and storage initialization | `print("Loading settings.py")`, `print(f"DEFAULT_FILE_STORAGE set to: {DEFAULT_FILE_STORAGE}")` | Logs showed `settings.py` loaded, `DEFAULT_FILE_STORAGE` set correctly.                      |
| Add debug prints to `storage.py`      | Added prints to trace `storage.py` import and instantiation            | `print("Loading storage.py")`, `print("Initializing CustomS3Boto3Storage")`                     | Initially missing, later appeared after forcing import, confirming import issue.             |
| Force import in `settings.py`         | Forced import of `CustomS3Boto3Storage` to catch errors                | `from sell_ur_stuff_site.storage import CustomS3Boto3Storage`                                   | Logs showed `Successfully imported CustomS3Boto3Storage`, confirming import works.           |
| Force instantiation in `settings.py`  | Forced instantiation to catch errors during `__init__`                 | `custom_storage = CustomS3Boto3Storage()`                                                       | Logs showed `CustomS3Boto3Storage initialized successfully`, confirming instantiation works. |
| Check `default_storage` after startup | Checked `default_storage` after forcing instantiation                  | `print(f"Storage backend at startup: {default_storage.__class__.__name__}")`                    | Still `FileSystemStorage`, indicating Django’s initialization issue persists.                |

### Solution Steps
| **Step**                            | **Action**                                                               | **Code/Change**                                                              | **Outcome**                                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Manually override `default_storage` | Set `default_storage` explicitly in `settings.py`                        | `default_storage = CustomS3Boto3Storage()`                                   | Logs showed `Manually set default_storage to: CustomS3Boto3Storage`, but override didn’t persist. |
| Patch `default_storage` lazy object | Patched the lazy object’s `_wrapped` attribute to ensure override sticks | `default_storage_original._wrapped = CustomS3Boto3Storage()`                 | `default_storage` now correctly set to `CustomS3Boto3Storage` at runtime.                         |
| Test storage backend                | Ran test to confirm `default_storage`                                    | `print(f"Storage class: {default_storage.__class__.__name__}")`              | Output: `Storage class: CustomS3Boto3Storage`, confirming fix.                                    |
| Test S3 upload                      | Uploaded a file via the `Sale` model                                     | `sale.main_image.save("test_image.jpg", ContentFile(b"Test image content"))` | File uploaded to S3 (`product_images/test_image.jpg`), confirmed with `head_object` (HTTP 200).   |

### Final Verification
| **Step**              | **Action**                                 | **Result**                                                                                                         | **Conclusion**                                        |
| --------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| Check `/market/` page | Visited `/market/` to verify image display | Image for “Test Item” should load from S3 (`https://sellyourtuff.s3.amazonaws.com/product_images/test_image.jpg`). | Images now display correctly, storage issue resolved. |

### Key Takeaways
- Django’s `DEFAULT_FILE_STORAGE` setting was not being applied due to a silent failure during startup, causing a fallback to `FileSystemStorage`.
- Forcing import and instantiation helped identify that `CustomS3Boto3Storage` itself was working, but Django’s initialization was the issue.
- Manually overriding `default_storage` and patching the lazy object ensured the correct storage backend was used at runtime.
- The fix was confirmed by a successful S3 upload and should resolve the issue of images not appearing on the `/market/` page.

---

This section provides a clear, tabular breakdown of the process, making it easy to follow the debugging and resolution steps.


---------------------------------------
---------------------------------------

## Resubmission Summary

This section outlines some of the key issues encountered and resolved for the resubmission.

### Resolved Issues:

1.  **Stripe API Authentication (Heroku):**
    *   **Symptom:** `stripe._error.AuthenticationError: Invalid API Key provided` in Heroku logs.
    *   **Fix:** Ensured `STRIPE_SECRET_KEY` was correctly set as a Heroku Config Var and that `stripe.api_key = os.getenv("STRIPE_SECRET_KEY")` (or `settings.STRIPE_SECRET_KEY`) was being initialized in `settings.py` before any Stripe API calls.

2.  **Gunicorn Worker Boot Failure (Heroku):**
    *   **Symptom:** `gunicorn.errors.HaltServer: <HaltServer 'Worker failed to boot.' 3>` in Heroku logs.
    *   **Fix:** Added `import stripe` at the top of `sell_ur_stuff_site/settings.py` to resolve a `NameError` during app startup.

3.  **Local Development Server - `ModuleNotFoundError`:**
    *   **Symptom:** `ModuleNotFoundError: No module named 'dotenv'` when running `python manage.py runserver`.
    *   **Fix:** Ensured the project's virtual environment (`.venv`) was activated in the terminal session before running Django management commands. The venv was located at `../.venv/` relative to the `sell_ur_stuff` project directory.

4.  **Django Template Syntax Error:**
    *   **Symptom:** `TemplateSyntaxError: Invalid block tag ... expected 'endblock'. Did you forget to register or load this tag?` pointing to an `{% endif %}`.
    *   **Fix:** Identified and added a missing `{% endif %}` tag for an `{% if highest_offer and sale.status == "available" %}` block within `sales/templates/sales/sale_detail.html`.

5.  **VS Code Python Interpreter Resolution:**
    *   **Symptom:** VS Code error `Failed to resolve env "/path/to/project/sell_ur_stuff/.venv/bin/python"`.
    *   **Fix:** Corrected the Python interpreter path in VS Code settings to point to the actual virtual environment location (`/Users/terryloughran/vs-projects-code-ins/.venv/bin/python`) which was one level above the Django project directory.

6.  **Heroku Python Version Warning:**
    *   **Symptom:** Heroku build log warning: `No Python version was specified`.
    *   **Fix:** Created a `.python-version` file in the project root directory with the content `3.13` to explicitly specify the Python version for Heroku builds.
  
7.  **Admin Panel Registration (Addressing Assessor Feedback LO1):**
*   **Symptom/Feedback:** "Furthermore those models present in the sales app have not been registered on the admin panel. Ensure to do so."
*   **Fix:** In `sales/admin.py`, imported the `Sale`, `Offer`, and `Purchase` models and registered them using `admin.site.register()`. This allows for easier management of these models through the Django admin interface.

This summary documents the troubleshooting process and key fixes applied to the project.
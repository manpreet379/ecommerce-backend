

class Constant:

    django_default_codes = {
        "required": 508,
        "blank": 508,
        "null": 508,
        "empty": 508,
    }

    response_messages = {

        500: "Internal server error.",
        501: "The requested API endpoint is not valid.",
        502: "The provided data is not in a valid JSON format.",
        503: "The 'Content-Type' header should be set to 'application/json'.",
        504: "User authentication failed.",
        505: "The requested HTTP method is not allowed.",
        506: "Sorry, you are not authorized to perform this action.",
        507: "Invalid parameter value provided.",
        508: "Required parameter or value is missing.",
        509: "User access token is expired or invalid.",
        510: "Your daily quota has been exhausted. Please try again later.",


        100: "User list fetched successfully.",
        101: "User created successfully.",
        102: "User creation failed.",
        103: "Logout successful.",
        104: "Logout failed.",
        105: "Password reset link sent to your email.",
        106: "User with this email does not exist.",
        107: "Invalid email address.",
        108: "Password reset successfully.",
        109: "Invalid token.",
        110: "User profile fetched successfully.",
        111: "User profile updated successfully.",
        112: "User profile update failed.",
        113: "Address list fetched successfully.",
        114: "Address created successfully.",
        115: "Address creation failed.",
        116: "Address fetched successfully.",
        117: "Address not found.",
        118: "Address updated successfully.",
        119: "Address update failed.",
        120: "Address deleted successfully.",
        130: "Category list fetched successfully.",
        131: "Category created successfully.",
        132: "Category creation failed.",
        133: "Product list fetched successfully.",
        134: "Product created successfully.",
        135: "Product creation failed.",
        136: "Product fetched successfully.",
        137: "Product updated successfully.",
        138: "Product update failed.",
        139: "Product deleted successfully.",
        140: "User registered successfully. Pending admin approval.",
        141: "User registration successfully.",
        142: "Pending Seller fetched successfully.",
        143: "Seller already approved.",
        144: "Seller approved successfully.",
        145: "Seller is already approved. Cannot reject.",
        146: "Seller rejected successfully.",



    }

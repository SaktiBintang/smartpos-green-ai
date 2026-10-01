/// Centralized constants used across the application.
class AppConstants {
  const AppConstants._();

  // Route Paths
  static const String loginRoute = '/login';
  static const String dashboardRoute = '/dashboard';

  // Secure Storage Keys
  static const String keyAccessToken = 'smartpos_access_token';
  static const String keyRefreshToken = 'smartpos_refresh_token';
  static const String keyCurrentMerchantId = 'smartpos_current_merchant_id';

  // Database
  static const String databaseName = 'smartpos_green_ai.sqlite';
}

/// Centralized application configuration.
///
/// Keeps environment variables and global runtime configuration in one place.
/// ARCHITECTURAL MANDATE: Gemini API key is NEVER embedded in the mobile client.
/// All AI queries and analytics are processed via the FastAPI backend.
class AppConfig {
  const AppConfig._();

  static const String appName = 'SmartPOS Green AI';
  static const String appTagline = 'From Transactions to Business Intelligence';
  static const String appVersion = '1.0.0';

  /// Backend REST API base URL.
  /// Overridable at compile time: --dart-define=API_BASE_URL=https://api.yourdomain.com/api/v1
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000/api/v1',
  );

  /// Network timeouts
  static const Duration connectTimeout = Duration(seconds: 15);
  static const Duration receiveTimeout = Duration(seconds: 15);
  static const Duration sendTimeout = Duration(seconds: 15);

  /// Offline Sync defaults
  static const int maxSyncRetries = 3;
}

import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'secure_token_storage.dart';

/// Contract interface for managing auth credentials in secure hardware storage.
abstract interface class TokenStorage {
  /// Store both access token and refresh token securely.
  Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  });

  /// Retrieve the current access token.
  Future<String?> getAccessToken();

  /// Retrieve the current refresh token.
  Future<String?> getRefreshToken();

  /// Check whether an active access token is present.
  Future<bool> hasAccessToken();

  /// Clear all stored auth tokens upon logout or session expiry.
  Future<void> clearTokens();
}

/// Provider exposing the active secure token storage implementation.
final tokenStorageProvider = Provider<TokenStorage>((ref) {
  return FlutterSecureTokenStorage();
});

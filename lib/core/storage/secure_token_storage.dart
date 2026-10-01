import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../constants/app_constants.dart';
import 'token_storage.dart';

/// Real implementation of [TokenStorage] backed by [FlutterSecureStorage].
/// Uses Android Keystore (encryptedSharedPreferences) and iOS Keychain.
class FlutterSecureTokenStorage implements TokenStorage {
  final FlutterSecureStorage _storage;

  FlutterSecureTokenStorage({FlutterSecureStorage? storage})
    : _storage =
          storage ??
          const FlutterSecureStorage(
            aOptions: AndroidOptions(resetOnError: true),
          );

  @override
  Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await Future.wait([
      _storage.write(key: AppConstants.keyAccessToken, value: accessToken),
      _storage.write(key: AppConstants.keyRefreshToken, value: refreshToken),
    ]);
  }

  @override
  Future<String?> getAccessToken() async {
    return _storage.read(key: AppConstants.keyAccessToken);
  }

  @override
  Future<String?> getRefreshToken() async {
    return _storage.read(key: AppConstants.keyRefreshToken);
  }

  @override
  Future<bool> hasAccessToken() async {
    return _storage.containsKey(key: AppConstants.keyAccessToken);
  }

  @override
  Future<void> clearTokens() async {
    await Future.wait([
      _storage.delete(key: AppConstants.keyAccessToken),
      _storage.delete(key: AppConstants.keyRefreshToken),
    ]);
  }
}

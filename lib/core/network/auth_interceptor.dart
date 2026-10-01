import 'package:dio/dio.dart';

import '../storage/token_storage.dart';

/// Interceptor that automatically injects the Bearer auth token into outgoing API requests.
class AuthInterceptor extends QueuedInterceptor {
  final TokenStorage _tokenStorage;

  AuthInterceptor(this._tokenStorage);

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    try {
      final token = await _tokenStorage.getAccessToken();
      if (token != null && token.isNotEmpty) {
        options.headers['Authorization'] = 'Bearer $token';
      }
    } catch (_) {
      // Fallback: proceed without token if secure storage read fails
    }
    return handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    // If a 401 is received, we can propagate or handle token refresh in the future phase
    return handler.next(err);
  }
}

import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../storage/token_storage.dart';
import 'api_client.dart';

/// Provider for the centralized [ApiClient].
final apiClientProvider = Provider<ApiClient>((ref) {
  final tokenStorage = ref.watch(tokenStorageProvider);
  return ApiClient(tokenStorage: tokenStorage);
});

/// Provider for raw [Dio] instance if required.
final dioProvider = Provider<Dio>((ref) {
  return ref.watch(apiClientProvider).dio;
});

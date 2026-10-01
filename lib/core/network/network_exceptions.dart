import 'package:dio/dio.dart';

/// Typed network exception hierarchy for clean error handling.
sealed class NetworkException implements Exception {
  final String message;
  final int? statusCode;

  const NetworkException({required this.message, this.statusCode});

  @override
  String toString() => message;

  /// Maps a DioException into a strongly-typed [NetworkException].
  factory NetworkException.fromDioException(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.transformTimeout:
        return const TimeoutNetworkException(
          message: 'Koneksi ke server timeout. Silakan periksa jaringan Anda.',
        );
      case DioExceptionType.connectionError:
        return const ConnectionNetworkException(
          message: 'Gagal terhubung ke server. Periksa koneksi internet Anda.',
        );
      case DioExceptionType.badResponse:
        final status = error.response?.statusCode;
        if (status == 401) {
          return UnauthorizedNetworkException(
            message:
                'Sesi telah berakhir atau tidak sah. Silakan login kembali.',
            statusCode: status,
          );
        } else if (status == 403) {
          return ForbiddenNetworkException(
            message: 'Akses ditolak.',
            statusCode: status,
          );
        } else if (status == 404) {
          return NotFoundNetworkException(
            message: 'Data atau endpoint tidak ditemukan.',
            statusCode: status,
          );
        } else if (status != null && status >= 500) {
          return ServerNetworkException(
            message: 'Terjadi kesalahan pada server. Silakan coba beberapa saat lagi.',
            statusCode: status,
          );
        }
        return BadResponseNetworkException(
          message:
              error.response?.statusMessage ??
              'Terjadi kesalahan pada respon server.',
          statusCode: status,
        );
      case DioExceptionType.cancel:
        return const RequestCancelledNetworkException(
          message: 'Permintaan dibatalkan.',
        );
      case DioExceptionType.badCertificate:
      case DioExceptionType.unknown:
        return UnknownNetworkException(
          message: error.message ?? 'Terjadi kesalahan yang tidak terduga.',
        );
    }
  }
}

class ConnectionNetworkException extends NetworkException {
  const ConnectionNetworkException({required super.message});
}

class TimeoutNetworkException extends NetworkException {
  const TimeoutNetworkException({required super.message});
}

class UnauthorizedNetworkException extends NetworkException {
  const UnauthorizedNetworkException({
    required super.message,
    super.statusCode,
  });
}

class ForbiddenNetworkException extends NetworkException {
  const ForbiddenNetworkException({required super.message, super.statusCode});
}

class NotFoundNetworkException extends NetworkException {
  const NotFoundNetworkException({required super.message, super.statusCode});
}

class ServerNetworkException extends NetworkException {
  const ServerNetworkException({required super.message, super.statusCode});
}

class BadResponseNetworkException extends NetworkException {
  const BadResponseNetworkException({required super.message, super.statusCode});
}

class RequestCancelledNetworkException extends NetworkException {
  const RequestCancelledNetworkException({required super.message});
}

class UnknownNetworkException extends NetworkException {
  const UnknownNetworkException({required super.message});
}

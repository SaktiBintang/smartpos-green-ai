import 'sync_status.dart';

/// Contract interface for domain entities participating in offline-first synchronization.
abstract interface class SyncableEntity {
  /// Unique identifier of the entity (UUID).
  String get id;

  /// Associated merchant tenant ID.
  String? get merchantId;

  /// Current sync status.
  SyncStatus get syncStatus;

  /// Timestamp when the record was last modified locally.
  DateTime get updatedAt;

  /// Convert entity to JSON map for sync transmission.
  Map<String, dynamic> toJson();
}

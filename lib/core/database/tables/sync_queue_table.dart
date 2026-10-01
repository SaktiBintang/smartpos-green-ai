import 'package:drift/drift.dart';

/// Foundation table for Offline-First Sync operations.
/// Stores mutations that occurred locally when offline and need synchronization
/// with the FastAPI backend once network connectivity is reestablished.
class SyncQueueEntries extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get merchantId => text().nullable()();
  TextColumn get entityType => text()(); // e.g. 'transaction', 'product'
  TextColumn get entityId => text()();
  TextColumn get operation => text()(); // 'create', 'update', 'delete'
  TextColumn get payload => text()(); // Serialized JSON
  TextColumn get status => text()(); // 'pending', 'syncing', 'failed', 'synced'
  IntColumn get retryCount => integer().withDefault(const Constant(0))();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
  DateTimeColumn get updatedAt => dateTime().withDefault(currentDateAndTime)();
}

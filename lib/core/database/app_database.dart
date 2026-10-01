import 'package:drift/drift.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'connection/open_connection.dart';
import 'tables/merchants_table.dart';
import 'tables/sync_queue_table.dart';

part 'app_database.g.dart';

/// Single centralized entry point for the local SQLite database via Drift.
/// Prepared for multi-merchant schema and offline-first data sync.
@DriftDatabase(tables: [Merchants, SyncQueueEntries])
class AppDatabase extends _$AppDatabase {
  AppDatabase([QueryExecutor? executor]) : super(executor ?? openConnection());

  @override
  int get schemaVersion => 1;

  @override
  MigrationStrategy get migration => MigrationStrategy(
    onCreate: (Migrator m) async {
      await m.createAll();
    },
    onUpgrade: (Migrator m, int from, int to) async {
      // Migration hooks for upcoming schema versions
    },
  );
}

/// Provider for the persistent [AppDatabase] instance.
final databaseProvider = Provider<AppDatabase>((ref) {
  final database = AppDatabase();
  ref.onDispose(() => database.close());
  return database;
});

/// Lifecycle statuses for local offline records awaiting cloud synchronization.
enum SyncStatus {
  /// Record created/modified locally, awaiting sync to FastAPI backend.
  pending,

  /// Record is currently being uploaded/processed by sync worker.
  syncing,

  /// Record is confirmed synchronized with PostgreSQL cloud database.
  synced,

  /// Sync attempt failed (network error, conflict, or server rejection).
  failed;

  static SyncStatus fromString(String value) {
    return SyncStatus.values.firstWhere(
      (e) => e.name == value,
      orElse: () => SyncStatus.pending,
    );
  }
}

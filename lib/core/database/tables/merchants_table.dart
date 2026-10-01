import 'package:drift/drift.dart';

/// Foundation table for Multi-Merchant architecture.
///
/// In subsequent phases, domain entities (transactions, inventory, customers)
/// will reference a [merchantId] to support multi-store or multi-tenant operations.
class Merchants extends Table {
  TextColumn get id => text()();
  TextColumn get name => text().withLength(min: 1, max: 100)();
  TextColumn get address => text().nullable()();
  TextColumn get phone => text().nullable()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
  DateTimeColumn get updatedAt => dateTime().withDefault(currentDateAndTime)();

  @override
  Set<Column> get primaryKey => {id};
}

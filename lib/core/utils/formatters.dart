/// General formatting utilities for POS operations.
class Formatters {
  const Formatters._();

  /// Formats numeric value into standard Indonesian Rupiah currency format.
  /// Example: 150000 -> "Rp 150.000"
  static String currency(num amount) {
    final isNegative = amount < 0;
    final absAmount = amount.abs().round();
    final str = absAmount.toString();
    final buffer = StringBuffer();

    for (int i = 0; i < str.length; i++) {
      if (i > 0 && (str.length - i) % 3 == 0) {
        buffer.write('.');
      }
      buffer.write(str[i]);
    }

    final formatted = buffer.toString();
    return isNegative ? '-Rp $formatted' : 'Rp $formatted';
  }

  /// Formats [DateTime] into a clean readable date string: DD/MM/YYYY
  static String date(DateTime dateTime) {
    final day = dateTime.day.toString().padLeft(2, '0');
    final month = dateTime.month.toString().padLeft(2, '0');
    final year = dateTime.year.toString();
    return '$day/$month/$year';
  }

  /// Formats [DateTime] into a clean readable date-time string: DD/MM/YYYY HH:mm
  static String dateTime(DateTime dateTime) {
    final d = date(dateTime);
    final hour = dateTime.hour.toString().padLeft(2, '0');
    final minute = dateTime.minute.toString().padLeft(2, '0');
    return '$d $hour:$minute';
  }
}

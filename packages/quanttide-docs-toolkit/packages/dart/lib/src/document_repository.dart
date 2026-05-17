import 'dart:async';

abstract class DocumentRepository {
  Future<String> read();
  Future<String> readFrom(String path);
  Future<void> write(String content);
  Stream<String> watch();
  Future<void> dispose();
}

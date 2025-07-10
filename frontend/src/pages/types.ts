export interface DocumentAPIModel {
  guid: string;
  filename: string;
  category: string;
  metadata: Record<string, string>;
}
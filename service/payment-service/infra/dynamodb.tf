resource "aws_dynamodb_table" "card_table" {
  name           = "payments"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Environment = "dev"
    Name        = "card-table"
  }
}

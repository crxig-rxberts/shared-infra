resource "aws_dynamodb_table" "card_table" {
  name           = "card-table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "cardNumber"
    type = "S"
  }

  global_secondary_index {
    name            = "CardNumberIndex"
    hash_key        = "cardNumber"
    projection_type = "ALL"
    read_capacity   = 5
    write_capacity  = 5
  }

  tags = {
    Environment = "dev"
    Name        = "card-table"
  }
}

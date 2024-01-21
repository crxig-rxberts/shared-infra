resource "aws_instance" "bisa_service" {
  ami                    = "ami-02cad064a29d4550c"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.bisa_service_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.bisa_service_profile.name
  depends_on             = [null_resource.build_app_image, aws_dynamodb_table.card_table]

  tags = {
    Name = "bisa-service"
  }

  user_data = templatefile("${path.module}/script/user_data.tpl", {
    dynamo_endpoint_url = "https://dynamodb.eu-west-1.amazonaws.com"
  })
}

resource "aws_security_group" "bisa_service_sg" {
  name        = "bisa-service-sg"
  description = "Allow ports 18080 and 22"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Custom port"
    from_port   = 18080
    to_port     = 18080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "bisa-service"
  }
}

resource "aws_iam_instance_profile" "bisa_service_profile" {
  name = "bisa-service-profile"
  role = aws_iam_role.bisa_service_role.name
}

resource "aws_iam_role_policy_attachment" "bisa_service_ecr_read_attachment" {
  role       = aws_iam_role.bisa_service_role.name
  policy_arn = aws_iam_policy.bisa_service_ecr_read_policy.arn
}

resource "aws_iam_role" "bisa_service_role" {
  name = "bisa-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      },
    ],
  })
}

resource "aws_iam_policy" "bisa_service_ecr_read_policy" {
  name        = "bisa-service-custom-policy"
  path        = "/"
  description = "Custom policy for EC2 to access specific services"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "cloudwatch:PutMetricData",
          "ssm:SendCommand",
          "ssm:GetParameter",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetAuthorizationToken",
          "ecr:DescribeRepositories",
          "dynamodb:*"
        ],
        Resource = "*"
      },
    ],
  })
}



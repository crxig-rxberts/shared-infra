resource "aws_ecr_repository" "payment_service" {
  name = "payment-service"
  force_delete = true
}

resource "null_resource" "build_app_image" {
  provisioner "local-exec" {
    command = "bash ./script/build_script.sh"
  }
  depends_on = [aws_ecr_repository.payment_service]

}
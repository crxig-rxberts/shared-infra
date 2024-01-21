resource "aws_ecr_repository" "bisa_service" {
  name = "bisa-service"
  force_delete = true
}

resource "null_resource" "build_app_image" {
  provisioner "local-exec" {
    command = "bash ./script/build_script.sh"
  }
  depends_on = [aws_ecr_repository.bisa_service]
}
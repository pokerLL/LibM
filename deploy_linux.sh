IMAGE="porkerll/libm:2.0"
docker build -t "${IMAGE}" -f Dockerfile .
docker push "${IMAGE}"


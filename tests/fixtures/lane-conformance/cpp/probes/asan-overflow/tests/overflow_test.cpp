int main() {
  int *values = new int[4];
  volatile int index = 4;
  int result = values[index];
  delete[] values;
  return result == 12345 ? 1 : 0;
}

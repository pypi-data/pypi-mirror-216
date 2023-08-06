lib:
lib.buildPythonPackage rec {
  pname = "types-psycopg2";
  version = "2.9.21.10";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "wmAIkjEq4cNOEvFFdJeV2T3E6sPvfb+KnBv9RThegNc=";
  };
}

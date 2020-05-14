## How to play around with DVC and asv?

1. Clone `dvc-test` repository.
2. `cd dvc-test`
3. `pip install -r requirements.txt`  (`virtualenv` has to be 16)
4. cd `asv_bench`
5. `dvc repro dvc.yaml:run_benchmarks`
6. `asv publish && asv preview`

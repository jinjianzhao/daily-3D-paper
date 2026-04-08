from run_pipeline import *

if __name__ == "__main__":
    my_api_key = os.getenv("MY_API_KEY")
    cfg = PipelineConfig()
    pipeline = PaperPipeline(my_api_key, cfg)
    today = datetime.now(timezone.utc)
    for i in range(0, 6):
        _day = today - timedelta(days=i)
        pipeline.run_pipeline(
            _day.strftime("%Y-%m-%d"), 
            # force_rerun=["step01", "step02", "step03", "step04", "step05", "step06", "step07", "step08", "step09"],
            skip_void_date=True,
        )
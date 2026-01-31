class PipelineException(Exception): pass
class DataExtractionError(PipelineException): pass
class DataTransformationError(PipelineException): pass
class StorageLoadError(PipelineException): pass

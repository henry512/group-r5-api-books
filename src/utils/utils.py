from typing import Any, List, Optional


class Utils:
    @staticmethod
    def chunk(data: List[Any], chunk_size: Optional[int] = 100) -> List[Any]:
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        return chunks

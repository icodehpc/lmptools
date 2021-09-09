from lmptools import DumpCallback, Dump
from lmptools.exceptions import SkipSnapshot

class MyCallback(DumpCallback):
	def on_snapshot_parse_timestamp(self, timestamp: int):
		if timestamp < 5000:
			raise SkipSnapshot(f"Skipping snapshot")

if __name__ == "__main__":
	d = Dump("dump.test.lammpstrj", unwrap=True, callback=MyCallback())
	res = d.parse()
	print(res)

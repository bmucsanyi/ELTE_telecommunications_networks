### How to run?

* Start the checksum server: python checksum_srv.py localhost 10101
* Start the netcopy server: python netcopy_srv.py localhost 11111 localhost 10101 1337 teszta.pdf
* Finally, start the netcopy client who wants to send data: python netcopy_cli.py localhost 11111 localhost 10101 1337 beam.pdf
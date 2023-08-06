# SimpleSplit

## Installation

```
pip3 install -r requirements.txt
```

## Usage

Split a file:

```
python3 simplesplit.py split --input large_file --output nonexistent_directory
```

Split file with a 1GB chunk size:

```
python3 simplesplit.py split --input large_file --output nonexistent_directory --chunk 1GB
```

Combine a file:

```
python3 simplesplit.py combine --input some_directory --output nonexistent_output_file
```

## License

Feel free to bundle this into your software, but please leave the in-code attribution.

Please make it clear if you change this program if you redistribute it.

Please don't license this software under a different license or sublicense it.

This software may be included in commercial software and/or other software as long as this package does not make up a significant portion of the software or is part of the core functionality.

THE LICENSE AND ANY ASSOCIATED SOFTWARE, DOCUMENTATION, OR SERVICES ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. THE ENTIRE RISK ARISING OUT OF THE USE OR PERFORMANCE OF THE LICENSE, SOFTWARE, DOCUMENTATION, OR SERVICES REMAINS WITH THE LICENSEE. IN NO EVENT SHALL THE LICENSOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE LICENSE, SOFTWARE, DOCUMENTATION, OR SERVICES, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

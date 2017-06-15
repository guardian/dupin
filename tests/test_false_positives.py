# coding=utf-8
import unittest

from dupin.trufflehog.false_positives import false_positive

class TestFalsePositives(unittest.TestCase):
    """Tweak these to suit your use case
    (See also /dupin/trufflehog/test_false_positives.py)
    """

    def test_returns_true_for_good_strings(self):
        self.assertFalse(false_positive("abc"))
        self.assertFalse(false_positive("123456"))
        self.assertFalse(false_positive("AKIAI6I5ULRC2RFJETXQ"))
        self.assertFalse(false_positive("key=AKIAI6I5ULRC2RFJETXQ"))
        self.assertFalse(false_positive("key: AKIAI6I5ULRC2RFJETXQ"))

    def test_resolved_yarn_things(self):
        self.assertTrue(false_positive('  resolved "https://registry.yarnpkg.com/url-to/something#1825d4e7ca220962959d35eb98851498bf476dd5"'))
        self.assertTrue(false_positive('  resolved "https://registry.yarnpkg.com/url-to/something/1825d4e7ca220962959d35eb98851498bf476dd5"'))
        self.assertTrue(false_positive('          "resolved": "git://github.com/substack/sockjs-client.git#10d48d06b4dba884416bf88a051f76ca3c8ffcae"'))

    def test__data_url_type_things(self):
        self.assertTrue(false_positive("//# sourceMappingURL=data:application/json;charset:utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9nbG9iYWwvZG9jdW1lbnQuanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwiZmlsZSI6ImdlbmVyYXRlZC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzQ29udGVudCI6WyJ2YXIgdG9wTGV2ZWwgPSB0eXBlb2YgZ2xvYmFsICE9PSAndW5kZWZpbmVkJyA/IGdsb2JhbCA6XG4gICAgdHlwZW9mIHdpbmRvdyAhPT0gJ3VuZGVmaW5lZCcgPyB3aW5kb3cgOiB7fVxudmFyIG1pbkRvYyA9IHJlcXVpcmUoJ21pbi1kb2N1bWVudCcpO1xuXG5pZiAodHlwZW9mIGRvY3VtZW50ICE9PSAndW5kZWZpbmVkJykge1xuICAgIG1vZHVsZS5leHBvcnRzID0gZG9jdW1lbnQ7XG59IGVsc2Uge1xuICAgIHZhciBkb2NjeSA9IHRvcExldmVsWydfX0dMT0JBTF9ET0NVTUVOVF9DQUNIRUA0J107XG5cbiAgICBpZiAoIWRvY2N5KSB7XG4gICAgICAgIGRvY2N5ID0gdG9wTGV2ZWxbJ19fR0xPQkFMX0RPQ1VNRU5UX0NBQ0hFQDQnXSA9IG1pbkRvYztcbiAgICB9XG5cbiAgICBtb2R1bGUuZXhwb3J0cyA9IGRvY2N5O1xufVxuIl19"))
        self.assertTrue(false_positive("        background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNSAxOCI+PHBhdGggZD0ibTggMC0xIDAtNyA3IDAgMTAgMSAxIDQgMCAwLTcgNSAwIDAgNyA0IDAgMS0xIDAtMTB6IiBmaWxsPSIjZmZmIiAvPjwvc3ZnPg==');"))
        self.assertTrue(false_positive("    src: url(data:application/font-woff;base64,09GRk9UVE8AASx8AAsAAAAC1iAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABDRkYgAABC7AAAnMMAANRfqNv5yEdQT1MAAN+wAAAv2QAA05h3vjRaR1NVQgABD4wAABcaAAAuHFlpQC9PUy8yAAABbAAAAFYAAABgbix102NtYXAAAD70AAAD5gAABVRy9uytaGVhZAAAAQgAAAA2AAAANvlMwaZoaGVhAAABQAAAACEAAAAkCDsG4GhtdHgAASaoAAAF1AAADLQxQYLObWF4cAAAAWQAAAAGAAAABgMtUABuYW1lAAABxAAAPTAAAOxhVr67GXBvc3QAAELcAAAAEAAAACAAAwBmAAEAAAABAACIax/qXw889QADA+gAAAAAxrHXGAAAAADPIqYX/z7+7AUjBKsAAAADAAIAAAAAAAB42mNgZGBg5v+vznCC1f+/3X8bVmUGoAgyYNYFAH2nBScAAAAAAFAAAy0AAHjaY2BhcmGcwMDKwMLUxRTBwMDgDaEZ4xjSGB0YGJjYWJlZWZnZOJiBcuwMSMDZ39eX8QCDwm8WZv7/6gwnWFYziigwMMwGyTGJMV0EUgoMPAAFgwvZAAB42sV9S4/jSJqYel+zjd1awIcFfNgF6DLszjJYWVU90zPdUz6MKlNZJWxWZo6krN46UhSl5KREakgqszWAT74YPvhiGIbPhg/7D/wX9rr7L3y1L7Yv/h7xxYtBPapr11OYTokiI7743q8I9nq9v/jiQ++LHv/v38D/+fMXvX8C3/jz7/V+0vsP6vPv9/557z+pz39g3fOHvX/d++/q8x/1/mnvf6nPP+kNvvhT9fmPe3/+xa/V5y97T7+Yq89/0vvLL/6d+vyn1ucnl//xi/+mPv9Z759dfQuzf/EHX8K3/3P1UX3+ovf0eqw+/17vz6436vPv9y6u/636/Ae9l9d/qz7/Ye+H6/+tPv+Rdf0nvX9/81v1+Y97/+rm/6rPX/bOf/0v1Oc/6f3y17n6/KfW5yf/5V/++r+qz3/We/M//vZvvn758tvnL7+LbpLNMnqTVEVWR0kxi87uqrxu8qSIxundY1I1v4ujTTHLqij7IV1u6vwhi5Z5mhV1FjWlvikto2GRnr44K1errErzZBlNtuvsNOovl1GVL+6aOqqyOqsestnp201SzXCKSfZDM1hs16NssVkm1avTly9fvj67fv/+tdwidzxXt3zIqjovi4hvvRlHL1/yx7uyScviAX84/eYXr1fJfVY289NlPv0arnz96tvvvukaU4OTAwoAygUgIKuyWdRUySxbJdV9VM4jb2UvvJV7P8d0cT9y75pm/csXLx4fH09TPUKDmIOv3pjRRVk00bicN/BoFg1gwFvAaHSpyNFfVFm2yormyZOby0F/PIhGg/55NHk3HEfn12e37wdXk+isPxpc3F5efiSAHjNYL00MX5q7pIm25Sa6z7I1YCIt19toXlbRfFM1dzBRlc0BL0UKZH3yZHIH6OqGITqBR6Kn+vvT6Ong9rIfw191L360foZ5nrZGefqMibLMFoCERA8+zZrHLCsIWlyHIQYjPo5mL6YvkqhFleQF/zBuTqM3VT7LBLPA49U2OknL5TJLG+Dy5TaOnnrPAzg42xRRhiSNpnkxy4sFoKoAZkl3AXYaEcYMghblQ1YVdYR4An5b1chlGxSrO5/UCVEni2ZZnS8KvE/uqaNsNS1neUY3VFletNbgDPX0WQxiu8iIno95cwdjb6NVBvwfR+sqLxoYaZUAPLDmOo4yHKkqizyNZmW6QcCTBgQQlMJ6BrfBLcls9rws8EPVPJbVfQxcNY1Q1IGazPc4R0lTytDMbKtkCxiLkrouAcc4NYGEi1tX5WwDCC3KR2QNWBdenW+aTZW1UCkEyeZzXnh0kjyLHu8UIZ72z"))

    def test_flow_type_sig(self):
        self.assertTrue(false_positive("// flow-typed signature: a37a0bc16c8494362f4a9481eb9657b2"))

    def test_sys_images(self):
        self.assertTrue(false_positive("                    '//i.guim.co.uk/img/static/sys-images/Guardian/Pix/contributor/2014/6/30/1404146756739/Polly-Toynbee-L.png?w=300&amp;q=85&amp;auto=format&amp;sharp=10&amp;s=abf0ce1a1a7935e82612b330322f5fa4',"))
        self.assertTrue(false_positive("                    '//i.guim.co.uk/img/static/sys-images/Guardian/Pix/pictures/2014/3/13/1394733739000/HughMuir.png?w=300&amp;q=85&amp;auto=format&amp;sharp=10&amp;s=c1eeb35230ad2a215ec9de76b3eb69fb',"))
        self.assertTrue(false_positive('        <img class="this-is-the-nhs__hand this-is-the-nhs__hand--left" src="@Configuration.static.path/sys-images/Guardian/Pix/pictures/2016/1/7/1452167267487/handleftcompressor.png" />'))
        self.assertTrue(false_positive('      Item700.bestFor(image) should be (Some(s"$imageHost/img/static/sys-images/Guardian/Pix/pictures/2013/7/5/1373023097878/b6a5a492-cc18-4f30-9809-88467e07ebfa-460x276.jpeg?w=700&q=55&auto=format&usm=12&fit=max&s=1e7d3c46056f162deec921e3c21de647"))'))
        self.assertTrue(false_positive('          endWith("img/static/sys-images/Guardian/Pix/audio/video/2014/5/16/1400240928538/Nigel-Farage-LBC-debate-i-014.jpg?w=640&h=360&q=85&auto=format&sharp=10&s=642bf1757bcb095c924d2f3789857019")'))
        self.assertTrue(false_positive('        "file":"http://static.guim.co.uk/sys-images/Guardian/About/General/2013/3/12/1363100797848/Meanwhile-back-in-the-liv-002.jpg",'))

    def test_gu_video(self):
        self.assertTrue(false_positive("        var desiredVideos = ['gu-video-111111111', 'gu-video-111111111111111111111111'];"))

    def test_json_allowed_hash(self):
        self.assertTrue(false_positive('    "shasum": "11a8a5685a63940d9d22b96fb2a5cef3b60b3830"'))
        self.assertTrue(false_positive('    "commit": "1111ee1c49d5ae4cf6097fc3f7cefedb9ad81bb5"'))
        self.assertTrue(false_positive('          "id": "1603edf3e4b0dad816840622",'))
        self.assertTrue(false_positive('                  "mediaId": "19b7ef3940bc0513a2aeabe5464b5d5c121225f0",'))

    def test_capi_test_fixtures(self):
        self.assertTrue(false_positive('{"response":{"status":"ok","userTier":"internal","total":1,"content":{"references":[],"elements":[{"id":"481724941056be27595bef042da48908029ec2ec","relation":"main","type":"image","assets":[{"type":"image","mimeType":"image/jpeg","file":"http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2015/2/5/1423136748039/6438e675-22b0-4ec2-b1fa-757c3b6b5a2f-220x132.jpeg","typeData":{"altText":"Vinyl collection","caption":"The nice thing about hi-fi separates is that you don’t have to buy everything at once. ","credit":"Photograph: John Wellings / Alamy/Alamy","photographer":"John Wellings / Alamy","source":"Alamy","width":"220","height":"132","secureFile":"https://static-secure.guim.co.uk/sys-images/Guardian/Pix/pictures/2015/2/5/1423136748039/6438e675-22b0-4ec2-b1fa-757c3b6b5a2f-220x132.jpeg","displayCredit":"true","mediaId":"481724941056be27595bef042da48908029ec2ec","imageType":"Photograph","suppliersReference":"CTKC0E","copyright":"Alamy","picdarUrn":"GD*49637217"}},{"type":"image","mimeType":"image/jpeg","file":"http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2015/2/5/1423136748509/6438e675-22b0-4ec2-b1fa-757c3b6b5a2f-460x276.jpeg","typeData":{"altText":"Vinyl collection","caption":"The nice thing about hi-fi separates is that you don’t have to buy everything at once. ","credit":"Photograph: John Wellings / Alamy/Alamy","photographer":"John Wellings / Alamy","source":"Alamy","width":"460","height":"276","secureFile":"https://static-secure.guim.co.uk/sys-images/Guardian/Pix/pictures/2015/2/5/1423136748509/6438e675-22b0-4ec2-b1fa-757c3b6b5a2f-460x276.jpeg","displayCredit":"true","mediaId":"481724941056be27595bef042da48908029ec2ec","imageType":"Photograph","suppliersReference":"CTKC0E","copyright":"Alamy","picdarUrn":"GD*49637217"}},{"type":"image","mimeType":"image/jpeg","file":"http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2015/2/5/1423136748696/6438e675-22b0-4ec2-b1fa-757c3b6b5a2f-540x324.jpeg","typeData":{"altText":"Vinyl collection","caption":"The nice thing about hi-fi separates is that you don’t have to buy everything at once. ","credit":"Photograph: John Wellings / Alamy/Alamy","photographer":"John Wellings / Alamy","source":"Alamy","width":"540","height":"324","secureFile":"https://static-secure.guim.co.uk/sys-images/Guardian/Pix/pictures/2015/2/5/1423136748696/6438e675-22b0-4ec2-b1fa-757c3b6b5a2f-540x324.jp...'))

    def test_media_url(self):
        self.assertTrue(false_positive('    images = List(HostedGalleryImage(url = "https://media.guim.co.uk/15494199050a52ed24f003f691e6abdd6eee5993/0_0_2048_1229/500.jpg", title = "", caption = "")),'))
        self.assertTrue(false_positive('          image = Some("http://media.guim.co.uk/1723e82cdd399f013905a5ee806fea3591b4a363/0_926_3872_1666/2000.jpg"),'))

    def test_frontend_static(self):
        self.assertTrue(false_positive('          "https://aws-frontend-static.s3.amazonaws.com/PROD/frontend-static/images/commercial/138c373fd249e5a2f4b6ae02e7cf3a93/renault-video-poster.jpg",'))

    def test_static_guim(self):
        self.assertTrue(false_positive('    <script src="http://static.guim.co.uk/static/1d5811c93d9b815024b5a6c3ec93a54be18e52f0/common/external-scripts/html5enable.js"></script>'))
        self.assertTrue(false_positive('            <a href="http://www.theguardian.com/uk"><img src="http://static.guim.co.uk/static/1d5811c93d9b815024b5a6c3ec93a54be18e52f0/common/images/logos/the-guardian/life-and-style.gif" width="115" height="22" alt="The Guardian home"></a>'))

    def test_github_reference(self):
        self.assertTrue(false_positive('[Read the Fronts architecture here](https://github.com/guardian/frontend/blob/14422b4537165424e70a898d150db4e806ba04d6/docs/02-architecture/02-fronts-architecture.md).'))
        self.assertTrue(false_positive('   * https://github.com/mozilla/rhino/commit/102abfed3f8ca043b2636efd31c14ba7552603dd'))

    def test_blend64(self):
        self.assertTrue(false_positive('        val imageOverlay = "&bm=normal&ba=bottom%2C%20left&bw=350&bp=20&blend64=aHR1cDovL1MxNC5wb3N0aW1nLm9yZy80YnA4cDJ4cjUvV2hpdGVfbG9nb193aXRoX3NoYWRvdy5wbmc"'))
        self.assertTrue(false_positive('  val blendImageParam = "blend64=aHR1cHM1Ly11cGxvYWRzLmd1aW0uY28udWsvMjAxNi8wNi8wNy9vdmVybGF5LWxvZ28tMTIwMC05MF9vcHQucG5n"'))

if __name__ == '__main__':
    unittest.main()

extern crate dexd;
extern crate structopt;
extern crate tempfile;
extern crate zip;

use std::fs::File;
use std::io::{self, Read};
use std::path::PathBuf;

use structopt::StructOpt;
use zip::ZipArchive;

#[derive(Debug, StructOpt)]
#[structopt(name = "apkdiff")]
struct Opt {
    /// First APK file
    #[structopt(parse(from_os_str))]
    apk1: PathBuf,
    /// Second APK file
    #[structopt(parse(from_os_str))]
    apk2: PathBuf,
}

fn main() -> io::Result<()> {
    let opt = Opt::from_args();

    let apk1_path = opt.apk1.as_path();
    let apk2_path = opt.apk2.as_path();

    if !apk1_path.exists() {
        eprintln!("{:?} does not exist", opt.apk1);
        std::process::exit(1);
    }

    if !apk2_path.exists() {
        eprintln!("{:?} does not exist", opt.apk2);
        std::process::exit(1);
    }

    let zipfile1 = File::open(&apk1_path)?;
    let mut archive1 = ZipArchive::new(zipfile1)?;
    let mut classes1 = archive1.by_name("classes.dex")?;
    let mut tmpfile1: File = tempfile::tempfile()?;
    io::copy(&mut classes1, &mut tmpfile1)?;

    let zipfile2 = File::open(&apk2_path)?;
    let mut archive2 = ZipArchive::new(zipfile2)?;
    let mut classes2 = archive2.by_name("classes.dex")?;
    let mut tmpfile2: File = tempfile::tempfile()?;
    io::copy(&mut classes2, &mut tmpfile2)?;

//    let d1 = read_dex_file(&mut tmpfile1);
  //  let d2 = read_dex_file(&mut tmpfile2);

    Ok(())
}

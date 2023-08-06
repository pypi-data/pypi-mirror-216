use pyo3::prelude::*;
use rayon::prelude::*;
use std::collections::HashMap;

/// Kmers start needs to be zero indexed
/// This cannot detect gaps. So ATCG != AT-CG, even the biological sequences are a match

// Private kmer class
struct Kmer {
    start: usize,
    seq: Vec<String>,
}
impl Kmer {
    fn new(start: usize, seq: Vec<String>) -> Self {
        Kmer { start, seq }
    }
    fn len(&self) -> usize {
        self.seq.iter().next().unwrap().chars().count()
    }
}

struct FKmer {
    end: usize,
    seq: Vec<String>,
}
impl FKmer {
    fn new(end: usize, seq: Vec<String>) -> Self {
        FKmer { end, seq }
    }
}

struct RKmer {
    start: usize,
    seq: Vec<String>,
}
impl RKmer {
    fn new(start: usize, seq: Vec<String>) -> Self {
        RKmer { start, seq }
    }
}

fn reverse_complement(seq: &str) -> String {
    let trans_hashmap: HashMap<char, char> = [('A', 'T'), ('T', 'A'), ('C', 'G'), ('G', 'C')]
        .iter()
        .copied()
        .collect();
    let mut complement_dna = String::new();
    for base in seq.chars().rev() {
        complement_dna.push(trans_hashmap[&base]);
    }
    return complement_dna;
}

fn generate_all_seqs(seqs: &Vec<String>) -> Vec<String> {
    let mut all_kmer_seqs: Vec<String> = seqs.iter().map(|s| s.to_owned()).collect();

    let r_seqs: Vec<String> = all_kmer_seqs
        .iter()
        .map(|s| reverse_complement(s))
        .collect();
    all_kmer_seqs.extend(r_seqs);

    return all_kmer_seqs;
}

fn generate_kmers(kmers: Vec<(usize, Vec<String>)>) -> Vec<Kmer> {
    // This generates the kmer class from a vector of deconstructed values
    // (start, seqs, msa_index) -> Kmer (start, seqs, msa_index)
    let mut kmer_list: Vec<Kmer> = Vec::new();
    for kmer in kmers.into_iter() {
        kmer_list.push(Kmer::new(kmer.0 as usize, kmer.1))
    }
    kmer_list
}

fn generate_fkmers(kmers: Vec<(usize, Vec<String>)>) -> Vec<FKmer> {
    // This generates the kmer class from a vector of deconstructed values
    // (start, seqs, msa_index) -> Kmer (start, seqs, msa_index)
    let mut kmer_list: Vec<FKmer> = Vec::new();
    for kmer in kmers.into_iter() {
        kmer_list.push(FKmer::new(kmer.0 as usize, kmer.1))
    }
    kmer_list
}
fn generate_rkmers(kmers: Vec<(usize, Vec<String>)>) -> Vec<RKmer> {
    // This generates the kmer class from a vector of deconstructed values
    // (start, seqs, msa_index) -> Kmer (start, seqs, msa_index)
    let mut kmer_list: Vec<RKmer> = Vec::new();
    for kmer in kmers.into_iter() {
        kmer_list.push(RKmer::new(kmer.0 as usize, kmer.1))
    }
    kmer_list
}

fn calc_sim_iter(seq1: &[u8], seq2: &[u8]) -> u32 {
    // This will return the number of simular bases, not consideering gaps
    return seq1
        .iter()
        .zip(seq2.iter())
        .map(|(s1, s2)| (s1 == s2) as u32)
        .sum::<u32>();
}

fn gen_digest_map(referance_seq: &Vec<String>) -> HashMap<(usize, usize), Vec<&[u8]>> {
    // This will generate a hashmap of digested seqs.
    // Kmer len will be K and V will be kmers

    // K is (reference index, kmer_size)
    let mut digest_hashmap: HashMap<(usize, usize), Vec<&[u8]>> = HashMap::new();

    for (ref_index, ref_seq) in referance_seq.iter().enumerate() {
        for kmer_len in 12..40 {
            digest_hashmap.insert(
                (ref_index, kmer_len as usize),
                kmer_digest(ref_seq.as_bytes(), kmer_len as usize),
            );
        }
    }

    return digest_hashmap;
}

fn kmer_digest(query: &[u8], k: usize) -> Vec<&[u8]> {
    // This will digest a sequence into all k-length sequences
    let mut return_vec: Vec<&[u8]> = Vec::new();
    for index in 0..query.len() - k + 1 {
        return_vec.push(&query[index..index + k])
    }
    return return_vec;
}

fn unique_rkmer(
    rkmer: &RKmer,
    digest_hashmap: &HashMap<(usize, usize), Vec<&[u8]>>,
    mismatch: u32,
    ref_index: usize,
) -> bool {
    // Generate all Kmer seqs
    let all_kmer_seqs = generate_all_seqs(&rkmer.seq);
    let kmer_slices: Vec<&[u8]> = all_kmer_seqs.iter().map(|a| a.as_bytes()).collect();

    // For each Kmer sequence
    for kmer_slice in kmer_slices {
        let kmer_slice_len = kmer_slice.len();
        let digested_kmers = digest_hashmap.get(&(ref_index, kmer_slice_len)).unwrap();

        let match_count: usize = digested_kmers
            .iter()
            .map(|dk| calc_sim_iter(kmer_slice, &dk))
            .filter(|sim_score| *sim_score >= (kmer_slice_len as u32) - mismatch)
            .count(); // This is the number of matches for this kmer, other than the expected binding site

        if match_count != 0 {
            return false;
        }
    }

    return true;
}

fn unique_rkmer_start(
    rkmer: &RKmer,
    digest_hashmap: &HashMap<(usize, usize), Vec<&[u8]>>,
    mismatch: u32,
    ref_index: usize,
) -> bool {
    // Generate all Kmer seqs
    let all_kmer_seqs = generate_all_seqs(&rkmer.seq);
    let kmer_slices: Vec<&[u8]> = all_kmer_seqs.iter().map(|a| a.as_bytes()).collect();

    // For each Kmer sequence
    for kmer_slice in kmer_slices {
        let kmer_slice_len = kmer_slice.len();

        let digested_kmers = digest_hashmap.get(&(ref_index, kmer_slice_len)).unwrap();

        let match_count: usize = digested_kmers
            .iter()
            .enumerate()
            .map(|(index, dk)| (index, calc_sim_iter(kmer_slice, &dk)))
            .filter(|(index, sim_score)| {
                *sim_score >= (kmer_slice_len as u32) - mismatch && *index != rkmer.start
            })
            .count(); // This is the number of matches for this kmer, other than the expected binding site

        if match_count != 0 {
            return false;
        }
    }

    return true;
}

fn unique_fkmer(
    fkmer: &FKmer,
    digest_hashmap: &HashMap<(usize, usize), Vec<&[u8]>>,
    mismatch: u32,
    ref_index: usize,
) -> bool {
    // Generate all Kmer seqs
    let all_kmer_seqs = generate_all_seqs(&fkmer.seq);
    let kmer_slices: Vec<&[u8]> = all_kmer_seqs.iter().map(|a| a.as_bytes()).collect();

    // For each Kmer sequence
    for kmer_slice in kmer_slices {
        let kmer_slice_len = kmer_slice.len();
        let digested_kmers = digest_hashmap.get(&(ref_index, kmer_slice_len)).unwrap();

        let match_count: usize = digested_kmers
            .iter()
            .map(|dk| calc_sim_iter(kmer_slice, &dk))
            .filter(|sim_score| *sim_score >= (kmer_slice_len as u32) - mismatch)
            .count(); // This is the number of matches for this kmer, other than the expected binding site

        if match_count != 0 {
            return false;
        }
    }

    return true;
}

fn unique_fkmer_start(
    fkmer: &FKmer,
    digest_hashmap: &HashMap<(usize, usize), Vec<&[u8]>>,
    mismatch: u32,
    ref_index: usize,
) -> bool {
    // Generate all Kmer seqs
    let all_kmer_seqs = generate_all_seqs(&fkmer.seq);
    let kmer_slices: Vec<&[u8]> = all_kmer_seqs.iter().map(|a| a.as_bytes()).collect();

    // For each Kmer sequence
    for kmer_slice in kmer_slices.iter() {
        let kmer_slice_len = kmer_slice.len();
        let digested_kmers = digest_hashmap.get(&(ref_index, kmer_slice_len)).unwrap();
        let match_count: usize = digested_kmers
            .iter()
            .enumerate()
            .map(|(index, dk)| (index, calc_sim_iter(kmer_slice, &dk)))
            .filter(|(index, sim_score)| {
                *sim_score >= (kmer_slice_len as u32) - mismatch
                    && *index != fkmer.end - kmer_slice_len
            })
            .count(); // This is the number of matches for this kmer, other than the expected binding site

        if match_count != 0 {
            return false;
        }
    }

    return true;
}

fn unique_kmer(
    kmer: &Kmer,
    digest_hashmap: &HashMap<(usize, usize), Vec<&[u8]>>,
    mismatch: u32,
    ref_index: usize,
) -> bool {
    let kmer_len = kmer.len();
    let all_kmer_seqs = generate_all_seqs(&kmer.seq);
    let kmer_slices: Vec<&[u8]> = all_kmer_seqs.iter().map(|a| a.as_bytes()).collect();
    // Turns the Kmers's String into &[u8]

    // For each Kmer sequence
    for kmer_slice in kmer_slices {
        // For each referance sequence
        let digested_kmers = digest_hashmap.get(&(ref_index, kmer_len)).unwrap();

        let match_count: usize = digested_kmers
            .iter()
            .map(|dk| calc_sim_iter(kmer_slice, &dk))
            .filter(|sim_score| *sim_score >= (kmer_len as u32) - mismatch)
            .count(); // This is the number of matches for this kmer, other than the expected binding site

        if match_count != 0 {
            return false;
        }
    }
    return true;
}

fn unique_kmer_start(
    kmer: &Kmer,
    digest_hashmap: &HashMap<(usize, usize), Vec<&[u8]>>,
    mismatch: u32,
    ref_index: usize,
) -> bool {
    let kmer_len = kmer.len();
    let all_kmer_seqs = generate_all_seqs(&kmer.seq);
    let kmer_slices: Vec<&[u8]> = all_kmer_seqs.iter().map(|a| a.as_bytes()).collect();
    // Turns the Kmers's String into &[u8]

    // For each Kmer sequence
    for kmer_slice in kmer_slices {
        // For each referance sequence
        let digested_kmers = digest_hashmap.get(&(ref_index, kmer_len)).unwrap();

        let match_count: usize = digested_kmers
            .iter()
            .enumerate()
            .map(|(index, dk)| (index, calc_sim_iter(kmer_slice, &dk)))
            .filter(|(index, sim_score)| {
                *sim_score >= (kmer_len as u32) - mismatch && *index != kmer.start
            })
            .count(); // This is the number of matches for this kmer, other than the expected binding site

        if match_count != 0 {
            return false;
        }
    }
    return true;
}

#[pyfunction]
fn rkmer_is_unique(
    rkmers: Vec<(usize, Vec<String>)>,
    referance_seqs: Vec<String>,
    n_cores: usize,
    mismatches: u32,
    detect_expected: bool,
) -> Vec<bool> {
    let rkmer_list = generate_rkmers(rkmers);
    let digest_hashmap = gen_digest_map(&referance_seqs);

    // Generate the thread pool
    rayon::ThreadPoolBuilder::new()
        .num_threads(n_cores)
        .build()
        .unwrap();

    let result_bool: Vec<bool> = rkmer_list
        .par_iter()
        .map(|rkmer| {
            let mut kmer_bools = Vec::new();
            for (ref_index, _) in referance_seqs.iter().enumerate() {
                match detect_expected {
                    true => {
                        kmer_bools.push(unique_rkmer(rkmer, &digest_hashmap, mismatches, ref_index))
                    }
                    false => kmer_bools.push(unique_rkmer_start(
                        rkmer,
                        &digest_hashmap,
                        mismatches,
                        ref_index,
                    )),
                };
            }
            // kmerbools is a bool for each ref seq (t,t,t)
            // This calls all on it
            kmer_bools.iter().all(|b| *b)
        })
        .collect();

    return result_bool;
}
#[pyfunction]
fn fkmer_is_unique(
    fkmers: Vec<(usize, Vec<String>)>,
    referance_seqs: Vec<String>,
    n_cores: usize,
    mismatches: u32,
    detect_expected: bool,
) -> Vec<bool> {
    let fkmer_list = generate_fkmers(fkmers);

    // Generate the thread pool
    rayon::ThreadPoolBuilder::new()
        .num_threads(n_cores)
        .build()
        .unwrap();

    let digest_hashmap = gen_digest_map(&referance_seqs);

    let result_bool: Vec<bool> = fkmer_list
        .par_iter()
        .map(|fkmer| {
            let mut kmer_bools = Vec::new();
            for (ref_index, _) in referance_seqs.iter().enumerate() {
                match detect_expected {
                    true => {
                        kmer_bools.push(unique_fkmer(fkmer, &digest_hashmap, mismatches, ref_index))
                    }
                    false => kmer_bools.push(unique_fkmer_start(
                        fkmer,
                        &digest_hashmap,
                        mismatches,
                        ref_index,
                    )),
                };
            }
            // kmerbools is a bool for each ref seq (t,t,t)
            // This calls all on it
            kmer_bools.iter().all(|b| *b)
        })
        .collect();

    return result_bool;
}

/// This will return a bool array of whever each kmer was unique, within the referance sequences, this version will
/// ignore_expected = True will ignore matches at the expected kmer start site
/// Mismatches is how many differances (excluding gaps) a kmer can have from the ref and still be called a hit
/// true means the kmer is unique
#[pyfunction]
fn kmer_is_unique(
    kmers: Vec<(usize, Vec<String>)>,
    referance_seqs: Vec<String>,
    n_cores: usize,
    mismatches: u32,
    detect_expected: bool,
) -> Vec<bool> {
    // This will ignore matches at fall at the expected index across all referance sequences
    let kmer_list = generate_kmers(kmers);
    let digest_hashmap = gen_digest_map(&referance_seqs);

    // Generate the thread pool
    rayon::ThreadPoolBuilder::new()
        .num_threads(n_cores)
        .build()
        .unwrap();

    let result_bool: Vec<bool> = kmer_list
        .par_iter()
        .map(|kmer| {
            let mut kmer_bools = Vec::new();
            for (ref_index, _) in referance_seqs.iter().enumerate() {
                match detect_expected {
                    true => {
                        kmer_bools.push(unique_kmer(kmer, &digest_hashmap, mismatches, ref_index))
                    }
                    false => kmer_bools.push(unique_kmer_start(
                        kmer,
                        &digest_hashmap,
                        mismatches,
                        ref_index,
                    )),
                };
            }
            // kmerbools is a bool for each ref seq (t,t,t)
            // This calls all on it
            kmer_bools.iter().all(|b| *b)
        })
        .collect();

    return result_bool;
}

/// A Python module implemented in Rust.
#[pymodule]
fn kmertools(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(kmer_is_unique, m)?)?;
    m.add_function(wrap_pyfunction!(rkmer_is_unique, m)?)?;
    m.add_function(wrap_pyfunction!(fkmer_is_unique, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_identical_calc_sim_iter() {
        let seq1 = "ATACGTAGCTGTAGCTG".as_bytes();
        assert_eq!(calc_sim_iter(seq1, seq1), seq1.len() as u32);
    }
    #[test]
    fn test_1dif_calc_sim_iter() {
        let seq1 = "ATACGTAGCTGTAGCTG".as_bytes();
        let seq2 = "ATACGTAGCTGAAGCTG".as_bytes();
        assert_eq!(calc_sim_iter(seq1, seq2), seq1.len() as u32 - 1);
    }
    #[test]
    fn test_digest_kmer_number() {
        // Test that it produces the correct number of kmers
        let ref_seq = "ATACGTAGCTGTAGCTGACTGATCGATCGTAGCTAGCTACGTCGATGCGTAGTCAGT".as_bytes();
        let k = 3;

        let kmers = kmer_digest(ref_seq, k);

        assert_eq!(kmers.len(), ref_seq.len() - k + 1);
    }
    #[test]
    fn test_digest_kmer_order() {
        // Test that ensure the kmers are correctly ordered
        let ref_seq = "ATACGTAGCTGTAGCTGACTGATCGATCGTAGCTAGCTACGTCGATGCGTAGTCAGT".as_bytes();
        let k = 3;

        let kmers = kmer_digest(ref_seq, k);

        // The first letter of each kmer should regenerate ref_seq[..ref_seq.len() - k]
        let kmer_first_letter: Vec<u8> = kmers.iter().map(|kmer| kmer[0]).collect();

        assert_eq!(
            *kmer_first_letter.as_slice(),
            ref_seq[..ref_seq.len() - k + 1]
        );
    }
    #[test]
    fn test_detect_repeat() {
        // Ensures that kmers are detected
        let ref_seqs = vec![
            "ATACGTAGCTGTAGCTGACTGATCGATCGTAGCTAGCTACGTCGATGCGTAGTCAGATCGATCGATGCTATGCT"
                .to_string(),
        ];
        let kmer = Kmer::new(0, vec!["ATACGTAGCTGTAGCTGACTG".to_string()]);
        let digest_hashmap = gen_digest_map(&ref_seqs);

        // See if the kmer Seq is found in the ref
        let data = unique_kmer(&kmer, &digest_hashmap, 0, 0);
        println!("Is Kmer Unique: {}", data);
        assert_eq!(data, false);
    }
    #[test]
    fn test_detect_repeat_ignore_start() {
        // Ensures that kmers are detected
        let ref_seqs = vec![
            "ATACGTAGCTGTAGCTGACTGATCGATCGTAGCTAGCTACGTCGATGCGTAGTCAGATCGATCGATGCTATGCT"
                .to_string(),
        ];
        let kmer = Kmer::new(0, vec!["ATACGTAGCTGTAGCTGACTG".to_string()]);
        let digest_hashmap = gen_digest_map(&ref_seqs);

        // See if the kmer Seq is found in the ref
        let data = unique_kmer_start(&kmer, &digest_hashmap, 0, 0);
        println!("Is Kmer Unique: {}", data);
        assert_eq!(data, true);
    }
    #[test]
    fn test_detect_ignore_start() {
        // Ensures that kmers are detected
        let ref_seqs = vec![
            "ATACGTAGCTGTAGCTGACTGATCGATCGTAGCTAGCTACGTCGATGCGTAGTCAGATCGATCGATGCTATGCT"
                .to_string(),
        ];
        let kmer = Kmer::new(1, vec!["ATACGTAGCTGTAGCTGACTG".to_string()]); // This Kmer should be detected
        let digest_hashmap = gen_digest_map(&ref_seqs);

        // See if the kmer Seq is found in the ref
        let data = unique_kmer_start(&kmer, &digest_hashmap, 0, 0);
        println!("Is Kmer Unique: {}", data);
        assert_eq!(data, false);
    }
    #[test]
    fn test_unique_rkmer_start() {
        // Ensures that expected kmers are not detected
        let ref_seqs = vec![
            "ATACGTAGCTGTAGCTGACTGATCGATCGTAGCTAGCTACGTCGATGCGTAGTCAGATCGATCGATGCTATGCT"
                .to_string(),
        ];
        let kmer = RKmer::new(0, vec!["ATACGTAGCTGTAGCTGACTG".to_string()]); // This Kmer should be detected
        let digest_hashmap = gen_digest_map(&ref_seqs);

        // See if the kmer Seq is found in the ref
        let data = unique_rkmer_start(&kmer, &digest_hashmap, 0, 0);

        assert_eq!(data, true);
    }
    #[test]
    fn test_rc() {
        let seq1 = "ATCG";
        let seq1_rc = "CGAT";

        assert_eq!(seq1_rc.to_string(), reverse_complement(seq1));
    }
    #[test]
    fn test_generate_all_seqs() {
        let seqs = vec!["ATCGTACT".to_string(), "TTCGTACT".to_string()];
        let all_seqs = generate_all_seqs(&seqs);

        println!("{:?}", all_seqs);

        assert_eq!(
            all_seqs,
            vec![
                "ATCGTACT".to_string(),
                "TTCGTACT".to_string(),
                "AGTACGAT".to_string(),
                "AGTACGAA".to_string()
            ]
        );
    }
    #[test]
    fn test_rkmer_detect() {
        let rkmer = RKmer::new(5, vec!["ATCGATCTGACTACGCATCGACGTA".to_string()]);

        let ref_seqs = vec![
            "ATACGTAGCTGTAGCTGACTGATCGATCGTAGCTAGCTACGTCGATGCGTAGTCAGATCGATCGATGCTATGCT"
                .to_string(),
        ];

        let digest_hashmap = gen_digest_map(&ref_seqs);
        let all_seqs = generate_all_seqs(&rkmer.seq);
        println!("{:?}", all_seqs);

        let result = unique_rkmer(&rkmer, &digest_hashmap, 0, 0);

        println!("{}", result);
    }
}

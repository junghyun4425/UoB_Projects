clear;

%% Task 1

% Get Snake mtDNA
snake_gbk = getgenbank('NC_007399');

% Copy the DNA sequence to a new variable mitochondria
snake = snake_gbk.Sequence;
snake_len = length(snake)

% Plot nt density
figure
ntdensity(snake)

bases = basecount(snake)

% Plot bases
figure
basecount(snake,'chart','pie');
title('Distribution of Nucleotide Bases for Snake Mitochondrial Genome');

% GC Content
gc_content = (bases.G + bases.C / snake_len) * 100

% Get CYTB / CYTC
% CYTB : 14969..16079
% CYTC : 6174..7775
% COx2 : 7899..8587
CYTB_gene = snake(14969:16079);
%COX1_gene = snake(6174:7775);
COX2_gene = snake(7899:8587);

CYTB_from_mtDNA = nt2aa(CYTB_gene, 'GeneticCode', 'Vertebrate Mitochondrial');
%COX1_from_mtDNA = nt2aa(COX1_gene, 'GeneticCode', 'Vertebrate Mitochondrial')
COX2_from_mtDNA = nt2aa(COX2_gene, 'GeneticCode', 'Vertebrate Mitochondrial');

% From TaxonomyBrowser
CYTB_from_web = "MPHHYILTLFGLLPVATNISTWWNFGSMLLTCLMLQVLTGFFLAVHYTANINLAFSSIIHITRDVPYGWLMQNLHAIGASMFFICIYIHIARGLYYGSHLNKETWVSGITLLITLMATAFFGYVLPWGQMSFWAATVITNLLTAVPYLGATMTTWLWGGFAINDPTLTRFFALHFILPFAIISLSSLHIILLHEEGSSNPLGTNPDIDKIPFHPYHSYKDLLLLTLMLLTLMITVSFFPDIFNDPDNFSKANPLITPQHIKPEWYFLFAYGILRSIPNKLGGALALVMSIMILLTAPLTHTAHLRPMTFRPLSQLMFWTLISTFITITWAATKPVEPPYIIISQATATLYFTFFISTPILGWIENKMMNS";
%COX1_from_web = "MYTTRWLFSTNHKDIGTLYLLFGAWSGLVGACLSVLMRMELTQPGSLFGSDQIFNVLVTAHAFVMIFFMVMPIMIGGFGNWLIPLMIGAPDMAFPRMNNMSFWLLPPALLLLLSSSYVEAGAGTGWTVYPPLSGNMVHSGPSVDLAIFSLHLAGASSILGAINFITTCVNMKPASMPMFNIPLFVWSVLITAIMLLLALPVLAAAITMLLTDRNLNTSFFDPSGGGDPVLFQHLFWFFGHPEVYILILPGFGIISSIITYYTGKKNTFGYTSMIWAMMSIAILGFVVWAHHMFTVGLDIDSRAYFTAATMIIAVPTGIKVFGWLATLTGGQIKWQTPIYWALGFIFLFTVGGMTGIILANSSLDIVLHDTYYVVAHFHYVLSMGAVFAIMGGVTHWFPLFTGYSLNQTLTKTQFWVMFLGVNMTFFPQHFLGLSGMPRRYSDFPDAFTLWNTISSIGSTISLVAVLMSLYIVWEAMTYKRTLPTPLGKKTHVEWFYGTPPPHHTHTEPTFMLNNMYAPIREYITYMEWPWPEK"
COX2_from_web = "MPYATQLSLQEGTGPAMEEVVFLHDHVLLLTFLMSLVILLFATTAITATVTHNDPTEEVEQLEAAWTAAPIMILILTALPSVRSLYLMEEVFDPYVTIKATGHQWYWNYEYTDGTNVSFDSYMIQTQDLPNGAPRLLEVDHRMVMPANLQTRIVVTAEDVLHSWALPSLGIKVDAVPGRLNQLPLATSRTGVFFGQCSEICGANHSFMPIVVEAVPLTYFEQWLLTTKQ";

if CYTB_from_mtDNA == CYTB_from_web
    fprintf("CYTB is same")
end

if COX2_from_mtDNA == COX2_from_web
    fprintf("COX2 is same")
end
%% Task 3
data = {'Python regius'                 'YP_313706';
        'Python anchietae'              'AIL52626';
        'Python bivittatus'             'AGL12235';
        'Xenopeltis unicolor'           'AAM83132';
        'Cylindrophis ruffus'           'AAL83566';
        'Anguilla rostrata'             'YP_164036';
        'Takydromus tachydromoides'     'YP_980177';
        'Crocodylus johnsoni'           'YP_004300406';
        };
NumCoV = length(data);
% CYTB Amino Acid
for ind = 1:NumCoV
    CoV_all(ind).Header   = data{ind,1};
    CoV_all(ind).Sequence = getgenpept(data{ind,2},'sequenceonly','true');
end

% Distance of CYTB
distances_CYTB = seqpdist(CoV_all,'Method','Jukes-Cantor','Alphabet','AA', 'squareform', true);
distances_CYTB

% CYTB_aa Tree
NJtree = seqneighjoin(distances_CYTB,'equivar',CoV_all);
sel = getbyname(NJtree,'crocodylus johnsoni');
RRtree = reroot(NJtree,sel);
plot(RRtree,'orient','left');
xlabel('Evolutionary Distance');
title('ReRooted Phylogenetic Tree (CYTB\_aa)');

%% Task 4
% CYTB data
data = {'Python regius'                 'YP_313706';
        'Cylindrophis ruffus'           'AAL83566';
        'Anguilla rostrata'             'YP_164036';
        'Takydromus tachydromoides'     'YP_980177';
        'Crocodylus johnsoni'           'YP_004300406';
        };
% CYTC data (COX1)
data2 = {'Python regius'                 'YP_313696';
         'Cylindrophis ruffus'           'YP_313722';
         'Anguilla rostrata'             'YP_164026';
         'Takydromus tachydromoides'     'YP_980167';
         'Crocodylus johnsoni'           'YP_004300396';
        };
    
NumCoV = length(data);
NumCoV2 = length(data2);

% CYTB Amino Acid
for ind = 1:NumCoV
    CoV(ind).Header   = data{ind,1};
    CoV(ind).Sequence = getgenpept(data{ind,2},'sequenceonly','true');
end

% CYTC Amino Acid
for ind = 1:NumCoV2
    CoV2(ind).Header   = data2{ind,1};
    CoV2(ind).Sequence = getgenpept(data2{ind,2},'sequenceonly','true');
end

% CYTB Nucleotide
for ind = 1:NumCoV
    CoV_nt(ind).Header = data{ind,1};
    CoV_nt(ind).Sequence = aa2nt(CoV(ind).Sequence, 'GeneticCode', 'Vertebrate Mitochondrial');
end

% CYTC Nucleotide
for ind = 1:NumCoV2
    CoV2_nt(ind).Header = data2{ind,1};
    CoV2_nt(ind).Sequence = aa2nt(CoV2(ind).Sequence, 'GeneticCode', 'Vertebrate Mitochondrial');
end

% Distance of CYTB_aa
distances_CYTB_aa = seqpdist(CoV,'Method','Jukes-Cantor','Alphabet','AA', 'squareform', true);
distances_CYTB_aa

% CYTB_aa Tree
NJtree = seqneighjoin(distances_CYTB_aa,'equivar',CoV);
sel = getbyname(NJtree,'crocodylus johnsoni');
RRtree_CYTB_aa = reroot(NJtree,sel);
plot(RRtree_CYTB_aa,'orient','left');
xlabel('Evolutionary Distance');
title('ReRooted Phylogenetic Tree (CYTB\_aa)');

% Distance of CYTC_aa (COX1)
distances_CYTC_aa = seqpdist(CoV2,'Method','Jukes-Cantor','Alphabet','AA', 'squareform', true);
distances_CYTC_aa

%% Task 5
% CYTC_aa Tree
NJtree = seqneighjoin(distances_CYTC_aa,'equivar',CoV2);
sel = getbyname(NJtree,'crocodylus johnsoni');
RRtree_CYTC_aa = reroot(NJtree,sel);
plot(RRtree_CYTC_aa,'orient','left');
xlabel('Evolutionary Distance');
title('ReRooted Phylogenetic Tree (CYTC\_aa)');

% Distance of CYTB_nt
distances_CYTB_nt = seqpdist(CoV_nt,'Method','Jukes-Cantor','Alphabet','NT', 'squareform', true);
distances_CYTB_nt
% CYTB_nt Tree
NJtree = seqneighjoin(distances_CYTB_nt,'equivar',CoV_nt);
sel = getbyname(NJtree,'crocodylus johnsoni');
RRtree_CYTB_nt = reroot(NJtree,sel);
plot(RRtree_CYTB_nt,'orient','left');
xlabel('Evolutionary Distance');
title('ReRooted Phylogenetic Tree (CYTB\_nt)');

% Distance of CYTC_nt (COX1)
distances_CYTC_nt = seqpdist(CoV2_nt,'Method','Jukes-Cantor','Alphabet','NT', 'squareform', true);
distances_CYTC_nt
% CYTC_nt Tree
NJtree = seqneighjoin(distances_CYTC_nt,'equivar',CoV2_nt);
sel = getbyname(NJtree,'crocodylus johnsoni');
RRtree_CYTC_nt = reroot(NJtree,sel);
plot(RRtree_CYTC_nt,'orient','left');
xlabel('Evolutionary Distance');
title('ReRooted Phylogenetic Tree (CYTC\_nt)');

% Consensus Tree
weights = [sum(distances_CYTB_aa) sum(distances_CYTB_nt) sum(distances_CYTC_aa) sum(distances_CYTC_nt)];
weights = weights / sum(weights);
consensus_dist = distances_CYTB_aa.* weights(1) + distances_CYTB_nt.* weights(2) + distances_CYTC_aa.* weights(3) + distances_CYTC_nt.* weights(4)

consensus_tree = seqlinkage(consensus_dist,'average',data(:,1));
sel = getbyname(consensus_tree,'crocodylus johnsoni');
RRconsensus_tree = reroot(consensus_tree,sel);
plot(RRconsensus_tree,'orient','left');
title('Consensus Tree');

%% Task 7
MultiAligned_CYTB = multialign(CoV);
seqalignviewer(MultiAligned_CYTB)

MultiAligned_COX1 = multialign(CoV2);
seqalignviewer(MultiAligned_COX1)